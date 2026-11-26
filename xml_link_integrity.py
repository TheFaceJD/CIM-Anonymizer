
import xml.etree.ElementTree as ET
from collections import Counter

INPUT_FILE = "input.xml"

RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
RDF_RESOURCE = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"


def check_links(filename):
    object_ids = set()
    references = set()
    id_counts = Counter()

    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            about = elem.attrib.get(RDF_ABOUT)
            resource = elem.attrib.get(RDF_RESOURCE)

            if about:
                object_ids.add(about)
                id_counts[about] += 1

            if resource:
                references.add(resource)

    internal = references & object_ids
    missing = references - object_ids

    duplicates = {
        object_id: count
        for object_id, count in id_counts.items()
        if count > 1
    }

    print("\nПРОВЕРКА СВЯЗЕЙ:")
    print("Количество уникальных объектов:", len(object_ids))
    print("Количество уникальных ссылок:", len(references))
    print("Ссылки на существующие объекты:", len(internal))
    print("Ссылки без найденного объекта:", len(missing))

    print("\nПРОВЕРКА УНИКАЛЬНОСТИ rdf:about:")
    print("Всего идентификаторов:", sum(id_counts.values()))
    print("Уникальных идентификаторов:", len(object_ids))
    print("Повторяющихся идентификаторов:", len(duplicates))

    if duplicates:
        print("\nПРИМЕРЫ ПОВТОРОВ:")
        for object_id, count in list(duplicates.items())[:20]:
            print(f"{object_id} — {count} раз")


if __name__ == "__main__":
    check_links(INPUT_FILE)
