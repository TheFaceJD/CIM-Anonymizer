
import json
from pathlib import Path


class UniqueRegistry:

    def __init__(self, filename="unique_registry.json"):
        self.filename = Path(__file__).resolve().parent / filename
        self.registry = {}
        self.used_values = {}

        if self.filename.exists():
            with open(self.filename, "r", encoding="utf-8") as file:
                self.registry = json.load(file)

            for key, value in self.registry.items():
                category = key.split(":", 1)[0]
                self.used_values.setdefault(category, {})[value] = key

    def get(self, object_id, category, generator):
        key = f"{category}:{object_id}"

        if key in self.registry:
            return self.registry[key]

        used = self.used_values.setdefault(category, {})
        attempt = 0

        while True:
            candidate = generator(object_id, attempt)

            if candidate not in used:
                self.registry[key] = candidate
                used[candidate] = key
                return candidate

            attempt += 1

    def save(self):
        temp_file = self.filename.with_suffix(".tmp")

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(
                self.registry,
                file,
                ensure_ascii=False,
                indent=2,
            )
            file.flush()

        temp_file.replace(self.filename)
