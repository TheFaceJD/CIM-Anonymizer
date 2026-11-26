
import xml.etree.ElementTree as ET
from collections import Counter

INPUT_FILE = "input.xml"
NAME_FIELD = "IdentifiedObject.name"


def local_name(tag):
    return tag.split("}")[-1]


def inspect_names(filename):
    counts = Counter()
    stack = []

    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            stack.append(local_name(elem.tag))
            continue

        if local_name(elem.tag) == NAME_FIELD and len(stack) >= 2:
            object_type = stack[-2]
            counts[object_type] += 1

        stack.pop()

    print("\nРАСПРЕДЕЛЕНИЕ НАЗВАНИЙ ПО CIM-КЛАССАМ:")

    for object_type, count in counts.most_common(100):
        print(f"{object_type}: {count}")

    print("\nВсего классов с полем name:", len(counts))
    print("Всего полей name:", sum(counts.values()))

    print("\nКЛАССЫ, НЕ ВКЛЮЧЁННЫЕ В ПРЕДВАРИТЕЛЬНЫЙ СПИСОК:")

    from sensitive_classes import get_name_category

    for object_type, count in counts.most_common():
        if get_name_category(object_type) is None:
            print(f"{object_type}: {count}")


if __name__ == "__main__":
    inspect_names(INPUT_FILE)
