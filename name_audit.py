
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
                if local_name(child.tag) == "IdentifiedObject.name":
                    if child.text and child.text.strip():
                        counts[object_type] += 1

            parent = elem.getparent()
            elem.clear()

            if parent is not None:
                while elem.getprevious() is not None:
                    del parent[0]

    return counts

print("Исходный файл...")
original = audit(BASE_DIR / "input.xml")

print("Анонимизированный файл...")
result = audit(BASE_DIR / "output_anonymized.xml")

print("\nКЛАССЫ И КОЛИЧЕСТВО НАЗВАНИЙ")
for object_type, total in original.most_common():
    print(
        f"{object_type}: "
        f"исходных {total}, "
        f"после {result[object_type]}"
    )
