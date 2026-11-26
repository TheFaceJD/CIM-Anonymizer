
from sensitive_classes import get_name_category

FIELD_RULES = {
    ("Person", "Person.firstName"): "PERSON",
    ("Person", "Person.lastName"): "PERSON",
    ("Person", "Person.middleName"): "PERSON",
    ("Person", "IdentifiedObject.name"): "PERSON",

    ("Organisation", "IdentifiedObject.name"): "ORGANIZATION",
    ("Organisation", "IdentifiedObject.description"): "DESCRIPTION",

    ("Customer", "IdentifiedObject.name"): "CUSTOMER",

    ("ServiceLocation", "IdentifiedObject.name"): "LOCATION",
    ("ServiceLocation", "Location.inChargeFullName"): "PERSON",
    ("ServiceLocation", "Location.mainAddress"): "ADDRESS",
    ("ServiceLocation", "Location.fiasId"): "ADDRESS_ID",
    ("ServiceLocation", "Location.fiasStreetId"): "ADDRESS_ID",

    ("Asset", "Asset.serialNumber"): "SERIAL",
    ("Meter", "Asset.serialNumber"): "SERIAL",
    ("Pole", "Asset.serialNumber"): "SERIAL",
    ("ProtectionEquipmentContainer", "Asset.serialNumber"): "SERIAL",
}

DESCRIPTION_CLASSES = {
    "ControlAreaOperator",
    "Position",
    "WorkOrderExecutionJournal",
    "Folder",
}

def get_field_category(parent_type, field_name):
    category = FIELD_RULES.get((parent_type, field_name))
    if category is not None:
        return category

    if field_name == "IdentifiedObject.name":
        return get_name_category(parent_type)

    if field_name == "IdentifiedObject.description":
        if parent_type in DESCRIPTION_CLASSES:
            return "DESCRIPTION"

    return None
