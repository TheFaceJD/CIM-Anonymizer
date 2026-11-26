
import xml.etree.ElementTree as ET
from collections import Counter

INPUT_FILE = "input.xml"

TARGETS = {
    "IdentifiedObject.name",
    "Asset.serialNumber",
    "Person.firstName",
    "Person.lastName",
    "Location.mainAddress",
    "Location.fiasId",
    "Location.fiasStreetId",
}


def local_name(tag):
    return tag.split("}")[-1]


def inspect(filename):
    counts = Counter()
    elements = []
    names = []

    for event, elem in ET.iterparse(
        filename, events=("start", "end")
    ):
        if event == "start":
            elements.append(elem)
            names.append(local_name(elem.tag))
            continue

        if names[-1] in TARGETS:
            # Имя CIM-класса — непосредственный
            # родитель целевого свойства
            if len(names) >= 2:
                object_type = names[-2]
                counts[(object_type, names[-1])] += 1

        if len(elements) >= 2:
            elements[-2].remove(elem)

        elem.clear()
        elements.pop()
        names.pop()

    print("\nПРИНАДЛЕЖНОСТЬ ПОЛЕЙ К CIM-КЛАССАМ:")

    for (object_type, field), count in sorted(counts.items()):
        print(f"{object_type} -> {field}: {count}")


if __name__ == "__main__":
    inspect(INPUT_FILE)
