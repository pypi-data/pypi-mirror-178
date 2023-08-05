from stratosphere.run import Run
from stratosphere.utils.assertions import assert_df, assert_no_field


def eval_metrics(run: Run):
    run.verify(assert_no_field("metrics"))
    run.verify(assert_df("predictions", columns=["y_true", "y_pred"]))

    metrics = {"accuracy": (run.fields["predictions"]["y_true"] == run.fields["predictions"]["y_pred"]).mean()}

    run.fields["metrics"] = metrics
