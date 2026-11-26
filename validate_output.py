
from pathlib import Path
from collections import Counter
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input.xml"
OUTPUT_FILE = BASE_DIR / "output_anonymized.xml"

RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
RDF_RESOURCE = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"


def scan_xml(path):
    object_ids = set()
    references = set()
    duplicate_ids = 0
    id_count = 0
    reference_count = 0

    context = etree.iterparse(
        str(path),
        events=("end",),
        huge_tree=True
    )

    for _, elem in context:
        object_id = elem.get(RDF_ABOUT)
        if object_id:
            id_count += 1
            if object_id in object_ids:
                duplicate_ids += 1
            object_ids.add(object_id)

        reference = elem.get(RDF_RESOURCE)
        if reference:
            reference_count += 1
            references.add(reference)

        parent = elem.getparent()
        elem.clear()

        if parent is not None:
            while elem.getprevious() is not None:
                del parent[0]

    return {
        "object_ids": object_ids,
        "references": references,
        "id_count": id_count,
        "reference_count": reference_count,
        "duplicate_ids": duplicate_ids,
    }


def main():
    print("Проверка исходного XML...")
    original = scan_xml(INPUT_FILE)

    print("Проверка анонимизированного XML...")
    anonymized = scan_xml(OUTPUT_FILE)

    print("\nРЕЗУЛЬТАТ ПРОВЕРКИ")
    print("Объектов в исходном файле:", original["id_count"])
    print("Объектов в результате:", anonymized["id_count"])

    print("Дубликаты ID в исходном файле:", original["duplicate_ids"])
    print("Дубликаты ID в результате:", anonymized["duplicate_ids"])

    print("Количество ссылок совпадает:",
          original["reference_count"] == anonymized["reference_count"])

    print("Набор ID совпадает:",
          original["object_ids"] == anonymized["object_ids"])

    print("Набор ссылок совпадает:",
          original["references"] == anonymized["references"])

    print("ID, отсутствующие в результате:",
          len(original["object_ids"] - anonymized["object_ids"]))

    print("Новые ID в результате:",
          len(anonymized["object_ids"] - original["object_ids"]))

    print("Изменённые ссылки:",
          len(original["references"] ^ anonymized["references"]))


if __name__ == "__main__":
    main()
