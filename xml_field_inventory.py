
from collections import Counter
from pathlib import Path
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input.xml"


def local_name(tag):
    if not isinstance(tag, str):
        return ""
    return tag.split("}")[-1]


def inspect_fields(filename):
    field_counts = Counter()
    attribute_counts = Counter()

    depth = 0
    root = None
    object_type = None

    context = etree.iterparse(
        str(filename),
        events=("start", "end"),
        huge_tree=True
    )

    for event, elem in context:
        if event == "start":
            depth += 1

            if depth == 1:
                root = elem

            elif depth == 2:
                object_type = local_name(elem.tag)

                for attr in elem.attrib:
                    attribute_counts[
                        (object_type, local_name(attr))
                    ] += 1

            elif depth == 3:
                field_name = local_name(elem.tag)
                field_counts[(object_type, field_name)] += 1

        else:
            if depth == 2:
                elem.clear()

                while elem.getprevious() is not None:
                    del root[0]

            elif depth > 2:
                elem.clear()

            depth -= 1

    print("\nПОЛЯ CIM-ОБЪЕКТОВ")
    print("Всего различных сочетаний класс/поле:", len(field_counts))

    print("\nПОЛЯ, КОТОРЫЕ ЧАСТО ВСТРЕЧАЮТСЯ:")

    for (class_name, field_name), count in field_counts.most_common(150):
        print(f"{class_name}.{field_name}: {count}")

    print("\nАТРИБУТЫ CIM-ОБЪЕКТОВ:")

    for (class_name, attr_name), count in attribute_counts.most_common(50):
        print(f"{class_name} / @{attr_name}: {count}")

    print("\nПОЛЯ АБОНЕНТОВ И СОТРУДНИКОВ:")

    target_classes = {
        "Person",
        "Customer",
        "Organisation",
        "Employee",
        "ServiceLocation",
        "TelephoneNumber",
        "ElectronicAddress",
    }

    for (class_name, field_name), count in sorted(field_counts.items()):
        if class_name in target_classes:
            print(f"{class_name}.{field_name}: {count}")

if __name__ == "__main__":
    inspect_fields(INPUT_FILE)
