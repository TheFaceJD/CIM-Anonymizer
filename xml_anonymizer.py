
from pathlib import Path
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input.xml"


def check_xml(input_file):
    print("Начинаем потоковую проверку XML...")

    count = 0

    try:
        for event, elem in etree.iterparse(
            str(input_file),
            events=("end",),
            huge_tree=True
        ):
            count += 1

            if count % 100000 == 0:
                print(f"Обработано элементов: {count:,}")

            # Освобождаем обработанный элемент из памяти
            elem.clear()

            parent = elem.getparent()
            if parent is not None:
                while elem.getprevious() is not None:
                    del parent[0]

        print("\nПроверка XML завершена успешно.")
        print(f"Всего обработано элементов: {count:,}")

    except etree.XMLSyntaxError as error:
        print("\nОшибка структуры XML:")
        print(error)

    except OSError as error:
        print("\nОшибка чтения файла:")
        print(error)


if __name__ == "__main__":
    if INPUT_FILE.exists():
        check_xml(INPUT_FILE)
    else:
        print("Ошибка: файл input.xml не найден.")
