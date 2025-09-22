# app/telemetry/mlflow_utils.py
import time
import mlflow
from contextlib import contextmanager
from app.config import settings

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_experiment(settings.MLFLOW_EXPERIMENT)

@contextmanager
def traced_run(name: str, params: dict | None = None):
    with mlflow.start_run(run_name=name):
        if params:
            mlflow.log_params(params)
        t0 = time.time()
        try:
            yield
        finally:
            mlflow.log_metric("latency_ms", (time.time() - t0) * 1000)

def log_chat(input_tokens: int | None, output_tokens: int | None, 
             tool_used: str | None, safety_flags: dict | None = None):
    if input_tokens is not None:
        mlflow.log_metric("input_tokens", input_tokens)
    if output_tokens is not None:
        mlflow.log_metric("output_tokens", output_tokens)
    if tool_used:
        mlflow.log_param("tool_used", tool_used)
    if safety_flags:
        for k, v in safety_flags.items():
            mlflow.log_param(f"safety_{k}", str(v))
