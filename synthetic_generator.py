
import hashlib
import json

from dictionaries import (
    MALE_FIRST_NAMES,
    FEMALE_FIRST_NAMES,
    MALE_LAST_NAMES,
    FEMALE_LAST_NAMES,
    MALE_MIDDLE_NAMES,
    FEMALE_MIDDLE_NAMES,
    STREETS,
    FRUIT_ADJECTIVES,
    VEGETABLE_ADJECTIVES,
)

from anonymizer import make_pseudonym
from unique_registry import UniqueRegistry

registry = UniqueRegistry()


def stable_index(value, category, size, attempt=0):
    data = f"{category}:{value}:{attempt}".encode("utf-8")
    digest = hashlib.sha256(data).digest()
    return int.from_bytes(digest[:8], "big") % size


def choose(values, value, category, attempt=0):
    if not values:
        raise ValueError(f"Пустой словарь: {category}")
    return values[stable_index(value, category, len(values), attempt)]


def unique_value(object_id, category, generator):
    return registry.get(str(object_id), category, generator)


def generate_person_parts(person_id, gender="male"):
    if gender == "female":
        first_names = FEMALE_FIRST_NAMES
        last_names = FEMALE_LAST_NAMES
        middle_names = FEMALE_MIDDLE_NAMES
    else:
        first_names = MALE_FIRST_NAMES
        last_names = MALE_LAST_NAMES
        middle_names = MALE_MIDDLE_NAMES

    def generator(value, attempt):
        parts = {
            "first": choose(first_names, value, "FIRST", attempt),
            "last": choose(last_names, value, "LAST", attempt),
            "middle": choose(middle_names, value, "MIDDLE", attempt),
        }
        return json.dumps(parts, ensure_ascii=False)

    result = unique_value(person_id, f"PERSON_{gender}", generator)
    return json.loads(result)


def anonymize_person_name(original_value, person_id):
    gender = (
        "female"
        if original_value.strip().lower().endswith(("а", "я"))
        else "male"
    )
    parts = generate_person_parts(person_id, gender)
    return f"{parts['last']} {parts['first']} {parts['middle']}"


def generate_person_email(person_id, person_parts):
    code = make_pseudonym(str(person_id), "EMAIL")
    return f"{person_parts['first'].lower()}.{code.lower()}@example.test"


def generate_address(original_value):
    def generator(value, attempt):
        street = choose(STREETS, value, "STREET", attempt)
        number = stable_index(value, "HOUSE", 900, attempt) + 100
        return f"ул. {street}, дом {number}"

    return unique_value(original_value, "ADDRESS", generator)


def generate_numeric_id(original_value, category, length):
    if length <= 0:
        raise ValueError("Неверная длина идентификатора")

    def generator(value, attempt):
        digest = hashlib.sha256(
            f"{category}:{value}:{attempt}".encode("utf-8")
        ).hexdigest()
        number = int(digest, 16) % (10 ** length)
        return str(number).zfill(length)

    return unique_value(original_value, category, generator)


def generate_object_name(original_value, object_id, object_type):
    def generator(value, attempt):
        fruit = choose(FRUIT_ADJECTIVES, value, "FRUIT", attempt)
        vegetable = choose(VEGETABLE_ADJECTIVES, value, "VEGETABLE", attempt)
        code = make_pseudonym(f"{value}:{attempt}", object_type)
        return f"{fruit} {vegetable} {code[-8:]}"

    return unique_value(object_id, object_type, generator)


def generate_organization_name(original_value, object_id):
    def generator(value, attempt):
        fruit = choose(FRUIT_ADJECTIVES, value, "ORG_FRUIT", attempt)
        code = make_pseudonym(f"{value}:{attempt}", "ORGANIZATION")
        return f"{fruit} организация {code[-8:]}"

    return unique_value(object_id, "ORGANIZATION", generator)


def generate_customer_name(original_value, customer_id):
    def generator(value, attempt):
        fruit = choose(FRUIT_ADJECTIVES, value, "CUSTOMER_FRUIT", attempt)
        vegetable = choose(
            VEGETABLE_ADJECTIVES, value, "CUSTOMER_VEGETABLE", attempt
        )
        code = make_pseudonym(f"{value}:{attempt}", "CUSTOMER")
        return f"{fruit} {vegetable} {code[-8:]}"

    return unique_value(customer_id, "CUSTOMER", generator)


def generate_description(original_value, object_id):
    return "Обезличенное описание " + make_pseudonym(
        str(object_id), "DESCRIPTION"
    )[-10:]


def generate_technical_name(original_value, object_id, object_type):
    return generate_object_name(original_value, object_id, object_type)


def generate_street(original_value):
    return generate_address(original_value)


def generate_person(original_value, gender="male"):
    parts = generate_person_parts(original_value, gender)
    return f"{parts['last']} {parts['first']} {parts['middle']}"
