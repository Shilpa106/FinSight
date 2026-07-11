import json
from pathlib import Path

from app.evals.evaluation_models import EvaluationCase


class EvaluationDatasetLoader:
    def load_dataset(self, path: str) -> tuple[str, list[EvaluationCase]]:
        dataset_path = Path(path)

        if not dataset_path.exists():
            raise FileNotFoundError(f"Evaluation dataset not found: {path}")

        with open(dataset_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        dataset_name = data["dataset_name"]
        cases = [EvaluationCase(**item) for item in data.get("cases", [])]

        return dataset_name, cases