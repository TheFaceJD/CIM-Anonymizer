
from pathlib import Path
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"

FIELDS = {
    "Person.firstName",
    "Person.lastName",
    "Person.middleName",
    "IdentifiedObject.name",
}

def local_name(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else ""

def read_persons(path):
    persons = {}
    context = etree.iterparse(
        str(path), events=("end",), huge_tree=True
    )

    for _, elem in context:
        if local_name(elem.tag) == "Person":
            object_id = elem.get(RDF_ABOUT)
            if object_id:
                fields = {}
                for child in elem:
                    name = local_name(child.tag)
                    if name in FIELDS and child.text:
                        fields[name] = child.text.strip()
                persons[object_id] = fields

            parent = elem.getparent()
            elem.clear()
            if parent is not None:
                while elem.getprevious() is not None:
                    del parent[0]

    return persons

original = read_persons(BASE_DIR / "input.xml")
result = read_persons(BASE_DIR / "output_anonymized.xml")

print("Количество Person:", len(original))
print("Количество Person в результате:", len(result))

for object_id, fields in original.items():
    new_fields = result.get(object_id, {})
    for field, old_value in fields.items():
        new_value = new_fields.get(field, "")
        print(
            field,
            "| изменено:", old_value != new_value,
            "| исходная длина:", len(old_value),
            "| новая длина:", len(new_value),
        )
