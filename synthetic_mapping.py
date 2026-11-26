
import json
import hmac
from pathlib import Path

from anonymizer import load_key


MAPPING_FILE = (
    Path(__file__).resolve().parent /
    "synthetic_mapping.json"
)


class SyntheticMapping:

    def __init__(self):
        self.key = load_key()
        self.mapping = {}

        if MAPPING_FILE.exists():
            with open(MAPPING_FILE, "r", encoding="utf-8") as file:
                self.mapping = json.load(file)

    def _source_key(self, category, original_id):
        """Создаёт защищённый ключ исходного объекта."""
        value = f"{category}:{original_id}".encode("utf-8")

        return hmac.new(
            self.key,
            value,
            "sha256"
        ).hexdigest()

    def get(self, category, original_id):
        """Получает ранее сохранённое синтетическое значение."""
        key = self._source_key(category, original_id)
        return self.mapping.get(key)

    def add(self, category, original_id, synthetic_value):
        """Сохраняет соответствие и проверяет уникальность."""

        key = self._source_key(category, original_id)

        if key in self.mapping:
            return self.mapping[key]

        for existing_key, existing_value in self.mapping.items():
            if (
                existing_value == synthetic_value
                and existing_key != key
            ):
                raise ValueError(
                    f"Коллизия синтетического значения: "
                    f"{synthetic_value}"
                )

        self.mapping[key] = synthetic_value

        return synthetic_value

    def save(self):
        """Сохраняет таблицу соответствий."""
        with open(MAPPING_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.mapping,
                file,
                ensure_ascii=False,
                indent=2
            )


if __name__ == "__main__":
    mapper = SyntheticMapping()

    first = mapper.add(
        "Substation",
        "test-object-001",
        "Вишнёвый Баклажанный_TEST001"
    )

    second = mapper.add(
        "Substation",
        "test-object-002",
        "Абрикосовый Картофельный_TEST002"
    )

    repeated = mapper.add(
        "Substation",
        "test-object-001",
        "Другое Название_TEST003"
    )

    mapper.save()

    print("Первый объект:", first)
    print("Второй объект:", second)
    print("Повтор первого объекта:", repeated)
    print("Повторяемость:", first == repeated)
    print("Количество записей:", len(mapper.mapping))
