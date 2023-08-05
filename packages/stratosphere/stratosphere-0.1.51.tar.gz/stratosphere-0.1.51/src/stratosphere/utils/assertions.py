import pandas as pd
from stratosphere.run import Run


class RunAssertion(Exception):
    """Raise this exception if an assertion on the runs state fails."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def assert_no_field(name):
    def func(run: Run):
        if name in run.fields:
            raise RunAssertion(f"Run field '{name}' already exists.")

    return func


def assert_field(name):
    def func(run: Run):
        if name not in run.fields:
            raise RunAssertion(f"Run field '{name}' does not exist.")

    return func


def assert_fields(names):
    def func(run: Run):
        for name in names:
            if name not in run.fields:
                raise RunAssertion(f"Run field '{name}' does not exist.")

    return func


def assert_type(name, field_type):
    def func(run: Run):
        if not isinstance(run.fields[name], field_type):
            raise RunAssertion(f"Run field '{name}' has type {type(run.fields[name])}, but {field_type} is expected.")

    return func


def assert_df(name, columns=None, n_rows=None):
    def func(run: Run):
        assert_field(name)
        assert_type(name, pd.DataFrame)
        if columns is not None:
            cols_df = set(run.fields[name].columns)
            cols_expected = set(columns)
            if cols_df != cols_expected:
                raise RunAssertion(
                    f"Run field '{name}' is a Pandas dataframe with columns {cols_df}, but {cols_expected} are"
                    " expected."
                )
        if n_rows is not None:
            n_rows_df = len(run.fields[name])
            if len(run.fields[name]) != n_rows:
                raise RunAssertion(
                    f"Run field '{name}' is a Pandas dataframe that contains {n_rows_df} rows, but {n_rows} are"
                    " expected."
                )

    return func
