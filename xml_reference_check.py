
import xml.etree.ElementTree as ET
from collections import Counter

INPUT_FILE = "input.xml"


def local_name(value):
    return value.split("}")[-1]


def inspect_references(filename):
    attribute_counts = Counter()
    attribute_examples = Counter()
    elements = []

    for event, elem in ET.iterparse(
        filename,
        events=("start", "end")
    ):
        if event == "start":
            elements.append(elem)

            for attribute, value in elem.attrib.items():
                attr_name = local_name(attribute)
                tag_name = local_name(elem.tag)

                attribute_counts[(tag_name, attr_name)] += 1

                if attr_name in ("about", "resource", "ID", "id"):
                    attribute_examples[(tag_name, attr_name)] += 1

        else:
            if len(elements) >= 2:
                elements[-2].remove(elem)

            elem.clear()
            elements.pop()

    print("\nАТРИБУТЫ XML:")

    for (tag, attribute), count in sorted(attribute_counts.items()):
        print(f"{tag} -> {attribute}: {count}")

    print("\nАТРИБУТЫ, ПОТЕНЦИАЛЬНО СОДЕРЖАЩИЕ ССЫЛКИ:")

    for (tag, attribute), count in sorted(attribute_examples.items()):
        print(f"{tag} -> {attribute}: {count}")


if __name__ == "__main__":
    inspect_references(INPUT_FILE)
