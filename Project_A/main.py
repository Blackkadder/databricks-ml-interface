"""
Project_A: Machine Learning Model Training Entry Point

This module contains the code to train an ML model and the dag_config
dictionary for Airflow Databricks operator to deploy the training job
as a Databricks job.
"""

import argparse
from typing import Any


def train_model(data_path: str, model_output_path: str, epochs: int = 10) -> dict[str, Any]:
    """
    Train a machine learning model.

    Args:
        data_path: Path to the training data.
        model_output_path: Path to save the trained model.
        epochs: Number of training epochs.

    Returns:
        Dictionary containing training metrics.
    """
    print(f"Loading data from: {data_path}")
    print(f"Training model for {epochs} epochs...")

    # Placeholder for actual ML training logic
    # In a real implementation, this would include:
    # - Data loading and preprocessing
    # - Model definition
    # - Training loop
    # - Model evaluation
    # - Model serialization

    metrics = {
        "accuracy": 0.95,
        "loss": 0.05,
        "epochs_completed": epochs,
    }

    print(f"Training complete. Model saved to: {model_output_path}")
    print(f"Metrics: {metrics}")

    return metrics


# Airflow Databricks operator configuration
# This configuration is used to deploy the training job as a Databricks job
dag_config = {
    "job_name": "Project_A_ML_Training",
    "description": "Machine learning model training job for Project_A",
    "tasks": [
        {
            "task_key": "train_model",
            "description": "Train the ML model",
            "spark_python_task": {
                "python_file": "dbfs:/projects/project_a/main.py",
                "parameters": [
                    "--data-path", "/dbfs/data/project_a/training_data",
                    "--model-output-path", "/dbfs/models/project_a/model",
                    "--epochs", "10",
                ],
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "num_workers": 2,
                "spark_conf": {
                    "spark.speculation": "true",
                },
            },
            "libraries": [
                {"pypi": {"package": "scikit-learn>=1.0.0"}},
                {"pypi": {"package": "pandas>=1.3.0"}},
                {"pypi": {"package": "numpy>=1.21.0"}},
            ],
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 0 8 * * ?",
        "timezone_id": "UTC",
    },
    "max_concurrent_runs": 1,
}


def main() -> None:
    """Main entry point for the training script."""
    parser = argparse.ArgumentParser(description="Train ML model for Project_A")
    parser.add_argument(
        "--data-path",
        type=str,
        default="/dbfs/data/project_a/training_data",
        help="Path to training data",
    )
    parser.add_argument(
        "--model-output-path",
        type=str,
        default="/dbfs/models/project_a/model",
        help="Path to save trained model",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs",
    )

    args = parser.parse_args()

    train_model(
        data_path=args.data_path,
        model_output_path=args.model_output_path,
        epochs=args.epochs,
    )


if __name__ == "__main__":
    main()
