from typing import Callable, List, Union

from stratosphere.store.db.database import next_ulid


class Run:
    """A run represents an instance of the experiment, obtained by
    combining the fixed and variable parameters. The Run objects
    (and the tracked fields)  must be serializable with cloudpickle.
    """

    def __init__(
        self,
        id_run: str = None,
        funcs: Union[Callable, List[Callable]] = None,
        kwargs: dict = None,
        params: dict = None,
        fields: dict = None,
    ):
        """Create a new run.

        Args:
            kwargs (dict, optional): Fixed parameters for all runs of an experiment. Defaults to None.
            parameters (dict, optional): Variable parameters to be considered for this run. Defaults to None.
            fields (dict, optional): fields to be tracked. Defaults to None.
            funcs (Union[Callable, List[Callable]], optional): One or more functions to be executed. Their
            only parameter is an instance of the Run class itself.
            experiment_name (str, optional): Name of the experiment the run belongs to. Defaults to None.
        """

        self.id_run = next_ulid() if id_run is None else id_run
        self.funcs = normalize_funcs(funcs)
        self.kwargs = {} if kwargs is None else kwargs
        self.params = {} if params is None else params
        self.fields = {} if fields is None else fields
        self.exception = None

    def execute(self, funcs=None):
        if funcs is not None:
            self.funcs = normalize_funcs(funcs)

        self.exception = None

        for func in self.funcs:
            try:
                func(self)
            except Exception as e:  # noqa
                # We want to catch all exceptions in the distributed execution of runs,
                # It will then be reported by Experiment.execute.
                self.exception = f"{func.__qualname__.split('.')[0]}: {str(e)}"
                break

        return self

    def verify(self, func):
        func(self)


def normalize_funcs(funcs):
    if funcs is None:
        return []
    elif callable(funcs):
        return [funcs]
    else:
        return funcs
