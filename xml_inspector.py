
import xml.etree.ElementTree as ET
from collections import Counter

INPUT_FILE = "input.xml"


def local_name(tag):
    return tag.split("}")[-1]


def inspect_xml(filename):
    object_types = Counter()
    field_counts = Counter()

    element_stack = []
    tag_stack = []

    target_types = {
        "Person",
        "Organisation",
        "Customer",
        "Substation",
        "Line",
        "StreetAddress",
        "StreetDetail",
        "ServiceLocation",
        "Location",
        "Asset",
    }

    for event, elem in ET.iterparse(filename, events=("start", "end")):

        if event == "start":
            element_stack.append(elem)
            tag_stack.append(local_name(elem.tag))
            continue

        depth = len(tag_stack)

        if depth == 2:
            object_type = tag_stack[-1]
            object_types[object_type] += 1

        elif depth == 3:
            object_type = tag_stack[-2]
            field_name = tag_stack[-1]

            if object_type in target_types:
                field_counts[(object_type, field_name)] += 1

        if depth >= 2:
            parent = element_stack[-2]
            try:
                parent.remove(elem)
            except ValueError:
                pass

        elem.clear()
        element_stack.pop()
        tag_stack.pop()

    print("\nТИПЫ ОБЪЕКТОВ:")
    for name, count in object_types.most_common(30):
        print(f"{name}: {count}")

    print("\nПОЛЯ ОБЪЕКТОВ ДЛЯ ОБЕЗЛИЧИВАНИЯ:")
    for (parent, field), count in sorted(field_counts.items()):
        print(f"{parent} -> {field}: {count}")


if __name__ == "__main__":
    inspect_xml(INPUT_FILE)
