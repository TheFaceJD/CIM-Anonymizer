
from pathlib import Path
from collections import Counter

from lxml import etree

from rules import get_field_category
from anonymizer import make_pseudonym
from synthetic_generator import (
    registry,
    generate_object_name,
    generate_organization_name,
    generate_address,
    generate_description,
    generate_numeric_id,
    generate_person_parts,
    generate_customer_name,
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input.xml"
OUTPUT_FILE = BASE_DIR / "output_anonymized.xml"

RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"

stats = Counter()


def local_name(tag):
    if not isinstance(tag, str):
        return ""
    return tag.split("}")[-1]


def get_object_id(elem):
    value = elem.get(RDF_ABOUT)
    if value:
        return value

    for child in elem:
        if local_name(child.tag) == "IdentifiedObject.mRIDStr":
            if child.text:
                return child.text

    return make_pseudonym(
        str(etree.tostring(elem, encoding="unicode")[:200]),
        "OBJECT_ID",
    )


def detect_gender(value):
    """Определяет пол по имени или отчеству."""
    if not value:
        return "male"

    value = value.strip().lower()

    if value.endswith((
        "овна", "евна", "ична", "инична",
        "на", "ова", "ева", "ина",
    )):
        return "female"

    return "male"


def get_person_parts(elem, object_id):
    """Создаёт единый набор синтетических частей ФИО для объекта."""
    first_name = None

    for child in elem.iter():
        if local_name(child.tag) == "Person.firstName":
            first_name = child.text
            break

    if first_name and first_name.strip():
        gender = (
            "female"
            if first_name.strip().lower().endswith(("а", "я"))
            else "male"
        )
    else:
        original_name = None

        for child in elem.iter():
            if local_name(child.tag) == "IdentifiedObject.name":
                original_name = child.text
                break

        gender = detect_gender(original_name)

    return generate_person_parts(object_id, gender)


def replace_value(
    value,
    category,
    object_id,
    object_type,
    field_name,
    person_parts=None,
):
    if value is None or not value.strip():
        return value

    if category == "TECHNICAL":
        return generate_object_name(value, object_id, object_type)

    if category == "ORGANIZATION":
        return generate_organization_name(value, object_id)

    if category == "ADDRESS":
        return generate_address(value)

    if category == "ADDRESS_ID":
        return generate_numeric_id(value, category, len(value))

    if category == "DESCRIPTION":
        return generate_description(value, object_id)

    if category == "PERSON":
        if person_parts is None:
            gender = detect_gender(value)
            person_parts = generate_person_parts(object_id, gender)

        if field_name == "Person.firstName":
            return person_parts["first"]

        if field_name == "Person.lastName":
            return person_parts["last"]

        if field_name == "Person.middleName":
            return person_parts["middle"]

        return (
            f"{person_parts['last']} "
            f"{person_parts['first']} "
            f"{person_parts['middle']}"
        )

    if category == "CUSTOMER":
        return generate_customer_name(value, object_id)

    if category == "SERIAL":
        digits = "".join(ch for ch in value if ch.isdigit())

        if digits and len(digits) == len(value):
            return generate_numeric_id(value, category, len(value))

    return make_pseudonym(value, category)


def process_xml():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Не найден файл: {INPUT_FILE}")

    if INPUT_FILE.resolve() == OUTPUT_FILE.resolve():
        raise ValueError("Входной и выходной файлы должны различаться.")

    depth = 0
    root = None
    root_writer = None
    has_child = False
    processed = 0

    context = etree.iterparse(
        str(INPUT_FILE),
        events=("start", "end", "pi", "comment"),
        huge_tree=True,
        remove_blank_text=False,
    )

    with etree.xmlfile(
        str(OUTPUT_FILE),
        encoding="UTF-8",
        buffered=True,
    ) as writer:

        writer.write_declaration()

        for event, elem in context:

            if event in ("pi", "comment"):
                if depth == 0:
                    writer.write(elem)
                continue

            if event == "start":
                depth += 1

                if depth == 1:
                    root = elem
                    root_writer = writer.element(
                        elem.tag,
                        attrib=dict(elem.attrib),
                        nsmap=elem.nsmap,
                    )
                    root_writer.__enter__()

                elif depth == 2 and not has_child:
                    writer.write(root.text or "")
                    has_child = True

                continue

            if depth == 2:
                object_type = local_name(elem.tag)
                object_id = get_object_id(elem)

                # Для Person создаём ФИО один раз на весь объект.
                person_parts = None
                if object_type == "Person":
                    person_parts = get_person_parts(elem, object_id)

                for child in elem.iter():
                    if child is elem:
                        continue

                    field_name = local_name(child.tag)

                    category = get_field_category(
                        object_type,
                        field_name,
                    )

                    if category is None:
                        continue

                    old_value = child.text

                    new_value = replace_value(
                        old_value,
                        category,
                        object_id,
                        object_type,
                        field_name,
                        person_parts,
                    )

                    if new_value != old_value:
                        child.text = new_value
                        stats[(object_type, field_name)] += 1

                tail = elem.tail or ""
                elem.tail = None
                writer.write(elem)

                if tail:
                    writer.write(tail)

                processed += 1
                elem.clear()

                while elem.getprevious() is not None:
                    del root[0]

                if processed % 100000 == 0:
                    print(f"Обработано объектов: {processed:,}")

            elif depth == 1:
                if not has_child:
                    writer.write(elem.text or "")

                root_writer.__exit__(None, None, None)

            depth -= 1

    registry.save()

    print("Реестр уникальных значений сохранён.")
    print("\nОбработка завершена.")
    print(f"Объектов обработано: {processed:,}")
    print(f"Результат: {OUTPUT_FILE}")

    print("\nИзменённые поля:")
    for (object_type, field_name), count in sorted(stats.items()):
        print(f"{object_type}.{field_name}: {count:,}")

    print(f"\nВсего изменено значений: {sum(stats.values()):,}")


if __name__ == "__main__":
    try:
        process_xml()
    except Exception as error:
        print(f"\nОШИБКА: {error}")
        raise
