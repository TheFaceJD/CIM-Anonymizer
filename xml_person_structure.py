
from pathlib import Path
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input.xml"

TARGET_CLASSES = {"Person", "Organisation", "Customer"}

def local_name(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else ""

def inspect(filename):
    depth = 0
    current_class = None
    fields = set()

    context = etree.iterparse(
        str(filename),
        events=("start", "end"),
        huge_tree=True
    )

    for event, elem in context:
        if event == "start":
            depth += 1

            if depth == 2:
                current_class = local_name(elem.tag)

            elif depth >= 3 and current_class in TARGET_CLASSES:
                fields.add((current_class, local_name(elem.tag)))

        else:
            if depth == 2:
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

            elif depth > 2:
                elem.clear()

            depth -= 1

    print("СТРУКТУРА ПОЛЕЙ:")
    for class_name, field_name in sorted(fields):
        print(f"{class_name}: {field_name}")

if __name__ == "__main__":
    inspect(INPUT_FILE)