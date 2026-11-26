
from pathlib import Path
from collections import Counter
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"

FIELDS = {
    "IdentifiedObject.name",
    "Asset.serialNumber",
    "IdentifiedObject.description",
    "Location.mainAddress",
    "Location.inChargeFullName",
    "Person.firstName",
    "Person.lastName",
    "Person.middleName",
}

def local_name(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else ""

def scan(path):
    result = {}
    context = etree.iterparse(
        str(path), events=("end",), huge_tree=True
    )

    for _, elem in context:
        object_id = elem.get(RDF_ABOUT)

        if object_id:
            fields = {}
            for child in elem.iter():
                field = local_name(child.tag)
                if field in FIELDS and child.text and child.text.strip():
                    fields.setdefault(field, []).append(child.text.strip())

            result[object_id] = fields

            parent = elem.getparent()
            elem.clear()
            if parent is not None:
                while elem.getprevious() is not None:
                    del parent[0]

    return result

print("Читаем исходный XML...")
original = scan(BASE_DIR / "input.xml")

print("Читаем результат...")
anonymized = scan(BASE_DIR / "output_anonymized.xml")

stats = Counter()

for object_id, fields in original.items():
    new_fields = anonymized.get(object_id, {})

    for field, old_values in fields.items():
        new_values = new_fields.get(field, [])

        for index, old_value in enumerate(old_values):
            stats[(field, "total")] += 1

            if index >= len(new_values):
                stats[(field, "missing")] += 1
            elif old_value == new_values[index]:
                stats[(field, "same")] += 1
            else:
                stats[(field, "changed")] += 1

print("\nРЕЗУЛЬТАТ СРАВНЕНИЯ")
for field in sorted(FIELDS):
    print(
        f"{field}: всего {stats[(field, 'total')]}, "
        f"изменено {stats[(field, 'changed')]}, "
        f"без изменений {stats[(field, 'same')]}, "
        f"отсутствует {stats[(field, 'missing')]}"
    )
