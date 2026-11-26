
from rules import get_field_category

tests = [
    ("Person", "Person.firstName"),
    ("Person", "Person.lastName"),
    ("Organisation", "IdentifiedObject.name"),
    ("Customer", "IdentifiedObject.name"),
    ("Substation", "IdentifiedObject.name"),
    ("SubstationSLD", "IdentifiedObject.name"),
    ("Line", "IdentifiedObject.name"),
    ("ACLineSegment", "IdentifiedObject.name"),
    ("PowerTransformer", "IdentifiedObject.name"),
    ("Discrete", "IdentifiedObject.name"),
    ("CurrentLimit", "IdentifiedObject.name"),
    ("ServiceLocation", "Location.mainAddress"),
    ("Asset", "Asset.serialNumber"),
    ("Meter", "Asset.serialNumber"),
]

if __name__ == "__main__":
    for parent_type, field_name in tests:
        category = get_field_category(parent_type, field_name)
        print(f"{parent_type} / {field_name} -> {category}")
