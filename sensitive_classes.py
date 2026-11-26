
ENERGY_OBJECT_CLASSES = {
    "Substation", "SubstationSLD", "Line", "ACLineSegment",
    "ACLineSeriesSection", "PowerTransformer", "PowerTransformerEnd",
    "Pole", "Bay", "VoltageLevel", "BusbarSection", "Disconnector",
    "GroundDisconnector", "Breaker", "Fuse", "LoadBreakSwitch",
    "SurgeArrester", "CurrentTransformer", "PotentialTransformer",
    "ProtectionEquipment", "ProtectionEquipmentContainer",
    "AutomaticRecloser", "Recloser", "Jumper", "Junction",
    "SynchronousMachine", "NonConformLoad", "WaveTrap",
    "CouplingCapacitor", "OperationalLimitSet", "GeographicalRegion",
    "SubGeographicalRegion", "HydroPowerPlant", "Plant",
    "ThermalGeneratingUnit", "WeatherStation", "Asset", "Meter",
    "UsagePoint", "Folder", "Department", "OperationalAuthority",
    "ControlAreaOperator", "Position", "WorkOrderExecutionJournal",
}

PERSON_CLASSES = {"Person"}
ORGANIZATION_CLASSES = {"Organisation"}
CUSTOMER_CLASSES = {"Customer"}

def get_name_category(parent_type):
    if parent_type in PERSON_CLASSES:
        return "PERSON"
    if parent_type in ORGANIZATION_CLASSES:
        return "ORGANIZATION"
    if parent_type in CUSTOMER_CLASSES:
        return "CUSTOMER"
    if parent_type in ENERGY_OBJECT_CLASSES:
        return "TECHNICAL"
    return None
