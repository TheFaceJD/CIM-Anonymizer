
from pathlib import Path
from collections import Counter
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"

def local_name(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else ""

def audit(path):
    counts = Counter()

    context = etree.iterparse(
        str(path), events=("end",), huge_tree=True
    )

    for _, elem in context:
        if elem.get(RDF_ABOUT):
            object_type = local_name(elem.tag)

            for child in elem.iter():
                if (
                    local_name(child.tag) == "IdentifiedObject.description"
                    and child.text
                    and child.text.strip()
                ):
                    counts[object_type] += 1

            parent = elem.getparent()
            elem.clear()

            if parent is not None:
                while elem.getprevious() is not None:
                    del parent[0]

    return counts

print("Анализируем исходный XML...")
counts = audit(BASE_DIR / "input.xml")

print("\nКЛАССЫ С ОПИСАНИЯМИ:")
for object_type, count in counts.most_common():
    print(f"{object_type}: {count}")

print("\nВсего описаний:", sum(counts.values()))
