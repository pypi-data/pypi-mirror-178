import logging
import random
from functools import partial
from typing import Callable, List, Union

import joblib
import pandas as pd
from sqlalchemy.orm import load_only
from stratosphere import config
from stratosphere.job import Job
from stratosphere.run import Run, normalize_funcs
from stratosphere.store import serialization
from stratosphere.store.db import models
from stratosphere.store.db.database import Database, next_ulid, pandas_query, sanitize_table_name
from stratosphere.utils import log
from stratosphere.utils.enums import IfExists, enforce_enum
from stratosphere.utils.environment import get_environment


class PickleNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RunException(Exception):
    """Raised if there's a failure during the execution of functions on runs."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ExperimentAlreadyExists(Exception):
    """Exception to handle the attempt to add one more experiment with the same name."""

    def __init__(self, name):
        self.message = f"Experiment '{name}' already existing, use if_exists=\"replace\" to overwrite it."
        super().__init__(self.message)


class ExperimentNotFoundException(Exception):
    """Exception raised if the experiment is not found."""

    def __init__(self, name):
        self.message = f"Experiment '{name}' not found. List with .ls() the available experiments."
        super().__init__(self.message)


class RunNotFoundException(Exception):
    """Exception raised if the run is not found."""

    def __init__(self, id_run):
        self.message = f"Run '{id_run}' not found. List with .df() the available runs."
        super().__init__(self.message)


class Experiment:
    """This class represents a new experiment.

    Raises:
        ExperimentNotFoundException: Raised if we try to use a non-existing experiment.
        ExperimentAlreadyExists: Raised if the experiment name is already present.

    Returns:
        Experiment: A defined experiment, ready to be executed, tracked, stored, queried.
    """

    # model_cls is the SQLAlchemy model mapped to this class.
    model_cls = models.Experiment

    def __init__(
        self,
        db: Database = None,
        id_experiment: str = None,
        name: str = None,
        funcs: Union[Callable, List[Callable]] = None,
        kwargs: dict = None,
        fields: dict = None,
        properties: dict = None,
        param_grid: List = None,
        runs: List[Run] = None,
    ):
        """Create a new experiment.

        Args:
            db (Database, optional): Database to link to. Defaults to None.
            id_experiment (str, optional): ID of the experiment to be used. Defaults to None.
            name (str, optional): Name of the experiment. Defaults to None.
            funcs (Union[Callable, List[Callable]], optional): One or more functions to call. Defaults to None.
            kwargs (dict, optional): Fixed parameters passed to the functions. Defaults to None.
            fields (dict, optional): Fixed experiment fields to be tracked. Defaults to None.
            properties (dict, optional): Experiment properties, used to hold meta-attributes. Defaults to None.
            param_grid (List, optional): Grid of parameters, used to generate the run parameters.
            runs (List[Run], optional): List of runs belonging to the experiment. Defaults to None.
        """

        self.db = db
        self.id_experiment = next_ulid() if id_experiment is None else id_experiment
        self.name = name
        self.funcs = normalize_funcs(funcs)
        self.kwargs = {} if kwargs is None else kwargs
        self.fields = {} if fields is None else fields

        # Populate properties
        self.properties = {} if properties is None else properties
        self.properties["environment"] = get_environment()

        # Populate param_grid
        self.param_grid = [{}] if (param_grid is None or param_grid == []) else param_grid
        if isinstance(self.param_grid, dict):
            self.param_grid = [self.param_grid]

        self.runs = runs

    def __reduce__(self):
        """
        Make the expriment pickable, avoiding unpickable objects in SQLAlchemy.

        Returns:
            Experiment: An unpickled Experiment object.
        """
        return self.__class__, (
            None,
            self.id_experiment,
            self.name,
            self.funcs,
            self.kwargs,
            self.fields,
            self.properties,
            self.param_grid,
            self.runs,
        )

    def table_name(self) -> str:
        """Return the table name of the experiment

        Returns:
            str: Table name
        """

        return sanitize_table_name(f"{config.db.experiment_table_prefix}{self.name}")

    @log.default_exception_handler
    def query(self, query: str = "SELECT * FROM {table_name}", verbose: bool = False) -> pd.DataFrame:
        """Query the experiment's table

        Args:
            query (str, optional): SQL query. {e} is replaced with the table name of the experiment.,
            {id} with the experiment ID, and {ee} with the experiments table. Defaults to the complete record.
            verbose (bool, optional): If true, print the resulting query. Defaults to False.

        Returns:
            pd.DataFrame: Result of the query.
        """

        df = self.db.pandas(
            query.format(
                id=f"'{self.id_experiment}'",
                table_name=self.table_name(),
                experiments_table=config.db.experiments_table,
                name=f"'{self.name}'",
            ),
            verbose=verbose,
        )

        return df

    def load_runs(self):
        # Retrieve all columns
        df = self.query()

        # Deserialize columns, if required
        for col_name in self.properties["run_fields"]["serialized"]:
            df[col_name] = df[col_name].map(serialization.deserialize)

        def series_to_run(row: pd.Series):
            fields = row[
                self.properties["run_fields"]["serialized"] + self.properties["run_fields"]["non_serialized"]
            ].to_dict()
            run = Run(id_run=row["id_run"], fields=fields)
            return run

        # Create runs and populate fields
        self.runs = df.apply(lambda row: series_to_run(row), axis=1).tolist()

    @classmethod
    def load_pickle(cls, db: Database, name: str):
        logging.info(f"Loading experiment '{name}' (pickle)")

        with db.session() as session:
            record = session.query(cls.model_cls).filter_by(name=name).first()
            if record is None:
                raise ExperimentNotFoundException(name)
            # Unpicke the serialized object.

            if record.pickle is None:
                raise PickleNotFoundException()

            experiment = serialization.pickle_loads(record.pickle)
            # Set the db of the experiment. Pickled db instances are never re-instantiated
            # completely, this let us reuse the existing database instance. See the Database
            # class for more comments on this.
            #
            # Important: this let us use SQLite memory databases, as only one instance is
            # used on all experiments.
            experiment.db = db
            return experiment

    @classmethod
    def load(cls, db: Database, name: str, pickle=False):
        """Load an experiment from database.

        Args:
            db (Database): Reference to a database.
            name (str): Name of the experiment.

        Raises:
            ExperimentNotFoundException: Raised if the experiment is not found.

        Returns:
            Experiment: Loaded experiment.
        """

        if pickle:
            return cls.load_pickle(db, name)

        logging.info(f"Loading experiment '{name}' (json-serialized)")

        # Create a new session
        with db.session() as session:
            record = session.query(cls.model_cls).filter_by(name=name).first()

            # If the record is not found, raise an error.
            if record is None:
                raise ExperimentNotFoundException(name)

            # Load the experiment from the record in "experiments" table.
            experiment = Experiment(
                db=db,
                id_experiment=record.id_experiment,
                name=record.name,
                fields=serialization.deserialize(record.fields),
                properties=serialization.deserialize(record.properties),
            )

            # Load the runs of the experiment, querying its table.
            experiment.load_runs()

            return experiment

    @log.default_exception_handler
    def execute(
        self,
        funcs: Union[Callable, List[Callable]] = None,
        backend=joblib.parallel.DEFAULT_BACKEND,
        n_jobs=-1,
    ):
        """Execute the experiment, then retuning it.

        Args:
            funcs (Union[Callable, List[Callable]], optional): Function(s) that will override the defined ones.
            If the value is "all", the re-evaluation of all defined functions is forced. Defaults to None.
            backend (_type_, optional): Joblib baackend. Defaults to joblib.parallel.DEFAULT_BACKEND.
            n_jobs (int, optional): Parallelization degree, defined as in Joblib. Defaults to -1.

        Returns:
            Run: the same experiment, ready for chained operations.
        """

        # Randomize the order of the runs to execute.
        random.shuffle(self.param_grid)

        if self.runs is None:
            # First execution: create runs and execute them.
            # If more functions are passed, we append them for execution.
            tasks = [
                partial(
                    lambda run: run.execute(funcs=funcs),
                    Run(kwargs=self.kwargs, params=params, funcs=self.funcs),
                )
                for params in self.param_grid
            ]
        else:
            tasks = [
                partial(
                    lambda run: run.execute(funcs=funcs),
                    run,
                )
                for run in self.runs
            ]

        if len(tasks) > 0:
            self.runs = Job(tasks, n_jobs=n_jobs, backend=backend).execute()

        # Check for exceptions, and report them if any.
        for run in self.runs:
            if run.exception is not None:
                raise RunException(run.exception)

        return self

    def record(
        self,
    ) -> models.Experiment:
        """Build an SQLAlchemy ORM object from the existing Experiment object.

        Returns:
            models.Experiment: SQLAlchemy ORM object.
        """

        return self.model_cls(
            id_experiment=self.id_experiment,
            name=self.name,
            fields=serialization.serialize(self.fields),
            properties=serialization.serialize(self.properties),
            pickle=serialization.pickle_dumps(self) if config.serialization.store_pickle else None,
        )

    def info(self):
        """Print some stats about the experiment.

        Returns:
            Experiment: self
        """
        logging.info("Experiment info")
        logging.info(f"  id...............: {self.id_experiment}")
        logging.info(f"  name.............: '{self.name}'")
        logging.info(f"  funcs............: {[func.__name__ for func in self.funcs]}")
        logging.info(f"  kwargs...........: {list(self.kwargs.keys())}")

        logging.info(f"  param_grid...: {list(self.param_grid[0].keys())} ({len(self.param_grid)})")

        logging.info(f"  fields...........: {list(self.fields.keys())}")
        logging.info(f"  size (Mb)........: {self.size('mb')} (compressed)")
        logging.info(f"  table name.......: {self.table_name()}")

        return self

    def get_field_columns(self):
        if len(self.runs) == 0:
            return []
        return list(self.runs[0].fields.keys())

    @log.default_exception_handler
    def persist(self, if_exists: IfExists = IfExists["fail"]):
        """Persist the experiment.

        Args:
            if_exists (IfExists, optional): Either "replace" or "fail". Defaults to "fail".

        Raises:
            ExperimentReadOnlyException: Experiment loaded in SQL read-only mode.

        Returns:
            _type_: self.
        """

        logging.info(f"Persisting experiment (table name: {self.table_name()})")

        if_exists = enforce_enum(if_exists, IfExists)

        # Delete record and table of experiment, honoring if_exists.
        self.delete(if_exists)

        # Prepare the fields of runs: we use .df() as starting point, limiting our analysis
        # to the field columns. The other columns are retained in the data frame, but are
        # ignored in the run_fields dict.
        df, run_fields = serialization.serialize_df(self.df(max_level=0), consider_columns=self.get_field_columns())

        # We save the fields structure as a property of the experiment, in the "experiments" table.
        self.properties["run_fields"] = run_fields

        # Insert row in "experiments" table.
        with self.db.session() as session:
            session.add(self.record())
            session.commit()

        dtype = {col_name: models.LargeBinary for col_name in run_fields["serialized"]}
        dtype["id_run"] = models.uuid_type
        dtype["id_experiment"] = models.uuid_type

        # Create the experiment table.
        self.db.pandas_to_sql(df, self.table_name(), if_exists.name, dtype=dtype)

        return self

    @log.default_exception_handler
    def lookup(self, id_run: str) -> Run:
        """Lookup a run by ID

        Args:
            id_run (str): ID of the run to lookup.

        Raises:
            RunNotFoundException: Raised if run ID not found.

        Returns:
            Run: The matching run.
        """

        if self.runs is None:
            raise RunNotFoundException(id_run)

        # A rather unperformance way to look up the run.
        # TODO: change .runs to a dict.
        for run in self.runs:
            if run.id_run == id_run:
                return run

    @log.default_exception_handler
    def delete(self, if_exists: IfExists = IfExists["fail"]) -> None:
        """Delete the expeirment.

        Args:
            if_exists (IfExists, optional): Either "replace" or "fail". In case
            the experiment exists and the value is "replace", nothing happens.
            If the experiment exists and the value is "fail", it will raise an
            exception. It is designed to work correctly together with insertions.
            Defaults to "fail".

        Raises:
            ExperimentAlreadyExists: Raised if the experiment exists.
        """

        if_exists = enforce_enum(if_exists, IfExists)

        # Create a new session
        with self.db.session() as session:
            # If we find the record ...
            if session.query(self.model_cls).filter_by(name=self.name).count() > 0:
                # And we are fine deleting it, proceed.
                if if_exists == IfExists["replace"]:
                    # We filter on matching experiment names, as these are the ones that might result
                    # in conflicts, since they must be unique.
                    session.query(Experiment.model_cls).filter(Experiment.model_cls.name == self.name).delete()
                else:
                    # Otherwise, raise an exception.
                    raise ExperimentAlreadyExists(self.name)
            session.commit()

        # We also need to drop the experiment table.
        self.db.drop_table(self.table_name())

    def df(self, max_level=None) -> pd.DataFrame:
        """Returns a Pandas dataframe representing the experiment, including
        parameters and fields. The processing does not depend on
        database queries, but the returned dataframe matches the contents
        of the experiment table (which is generated using this method).

        In presence of overlapping column names from the fixed fields
        of the experiment and the run fields, the fields use
        "_run" as suffix.

        Args:
            include_experiment (bool, optional): If False, do not include the
            fixed experiment fields (it will be a constant column).
            Defaults to True.

        Raises:
            ExperimentReadOnlyException: Experiment loaded in SQL read-only mode.

        Returns:
            pd.DataFrame: Pandas dataframe representing the tracked properties.
        """

        # Load the dataframe from a dict or list of dicts.
        df_runs = pd.json_normalize(
            [{**run.fields, **{"id_run": run.id_run}} for run in self.runs], max_level=max_level
        )

        df_experiment = pd.json_normalize(
            {
                **self.fields,
                **{"id_experiment": self.id_experiment, "name": self.name},
            }
        )

        if len(set(df_runs.columns).intersection(df_experiment.columns)) > 0:
            raise Exception(
                f"Duplicate column names: {set(df_runs.columns).intersection(df_experiment.columns)}. You might have"
                " experiment fields named as run fields."
            )

        df = df_experiment.merge(
            df_runs,
            how="cross",
        )

        return reorder_columns(df, ["name", "id_experiment", "id_run"]).apply(pd.to_numeric, errors="ignore")

    def size(self, unit: str = "b") -> int:
        """Return the size of the pickled version of the expeirment.

        Args:
            unit (str, optional): Unit of measure: "b" (Bytes), "kb" (KiloBytes), "mb" (MegaBytes). Defaults to "b".

        Returns:
            int: Size of the experiment once pickled.
        """
        return serialization.pickle_size(self, unit=unit)

    @classmethod
    def ls(cls, db: Database, include_properties=False) -> pd.DataFrame:
        """List experiments in a database.

        Args:
            db (Database): Database instance.

        Returns:
            pd.DataFrame: List of experiments.
        """

        # Construct list of columns to retrieve
        if include_properties:
            columns = [Experiment.model_cls.id_experiment, Experiment.model_cls.name, Experiment.model_cls.properties]
        else:
            columns = [Experiment.model_cls.id_experiment, Experiment.model_cls.name]

        with db.session() as session:
            df_experiments = pandas_query(
                session.query(Experiment.model_cls).options(load_only(*columns)),
                session,
            )

            df_experiments["table_name"] = df_experiments["name"].apply(
                lambda name: sanitize_table_name(f"{config.db.experiment_table_prefix}{name}")
            )

            if include_properties:
                df_experiments["properties"] = df_experiments["properties"].map(serialization.deserialize)
                df_experiments = serialization.explode_json_column(df_experiments, col_name="properties")

            return df_experiments


def reorder_columns(df: pd.DataFrame, ordered_columns: List[str]) -> List[str]:
    """Given a dataframe, enforce a partial ordering of some columns, appending
    the remaining ones in sorted order.

    Args:
        df (pd.DataFrame): Consider the columns from thsi dataframe.
        ordered_columns (List[str]): Consider this partial ordering of the columns.

    Returns:
        List[str]: New ordering of all columns for the {df} dataframe.
    """

    remaining_columns = sorted([col_name for col_name in df.columns if col_name not in ordered_columns])
    return df[ordered_columns + remaining_columns]
