
from pathlib import Path
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"

TARGET_CLASSES = {
    "Organisation",
    "Folder",
    "WorkOrderExecutionJournal",
    "Position",
    "ControlAreaOperator",
    "Department",
    "OperationalAuthority",
    "ServiceLocation",
    "GeographicalRegion",
    "SubGeographicalRegion",
    "HydroPowerPlant",
    "Plant",
    "WeatherStation",
    "Asset",
}

TARGET_FIELDS = {
    "IdentifiedObject.name",
    "IdentifiedObject.description",
}

def local_name(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else ""

def audit(path):
    count = {}

    context = etree.iterparse(
        str(path), events=("end",), huge_tree=True
    )

    for _, elem in context:
        object_type = local_name(elem.tag)

        if elem.get(RDF_ABOUT) and object_type in TARGET_CLASSES:
            for child in elem.iter():
                field = local_name(child.tag)

                if (
                    field in TARGET_FIELDS
                    and child.text
                    and child.text.strip()
                ):
                    key = (object_type, field)
                    count[key] = count.get(key, 0) + 1

            parent = elem.getparent()
            elem.clear()

            if parent is not None:
                while elem.getprevious() is not None:
                    del parent[0]

    return count

result = audit(BASE_DIR / "input.xml")

print("КОНТРОЛЬ ЧУВСТВИТЕЛЬНЫХ КЛАССОВ\n")

for (object_type, field), number in sorted(result.items()):
    print(f"{object_type}.{field}: {number}")

print("\nВсего найдено полей:", sum(result.values()))
