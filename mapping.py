
import json
import os

from anonymizer import make_pseudonym


MAPPING_FILE = "anonymization_mapping.json"


class AnonymizationMapping:

    def __init__(self):
        self.mapping = {}

        if os.path.exists(MAPPING_FILE):
            with open(MAPPING_FILE, "r", encoding="utf-8") as file:
                self.mapping = json.load(file)

    def get(self, value, category):
        if value is None or value == "":
            return value

        key = f"{category}:{value}"

        if key not in self.mapping:
            self.mapping[key] = make_pseudonym(value, category)

        return self.mapping[key]

    def save(self):
        with open(MAPPING_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.mapping,
                file,
                ensure_ascii=False,
                indent=2
            )


if __name__ == "__main__":
    mapper = AnonymizationMapping()

    first = mapper.get("Иван Иванов", "PERSON")
    second = mapper.get("Иван Иванов", "PERSON")
    third = mapper.get("Петр Петров", "PERSON")

    mapper.save()

    print("Первое значение:", first)
    print("Повторное значение:", second)
    print("Другое значение:", third)
    print("Совпадение:", first == second)
    print("Количество записей:", len(mapper.mapping))
