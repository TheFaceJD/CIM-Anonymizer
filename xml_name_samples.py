
import xml.etree.ElementTree as ET
from collections import defaultdict

INPUT_FILE = "input.xml"
TARGET_CLASSES = {
    "OperationalLimitSet", "CurrentLimit", "Discrete",
    "VoltageLimit", "CurrentVsTemperatureLimitCurve",
    "TransformerMeshImpedance", "ShortCircuitTestME",
    "NoLoadTestME", "RatioTapChanger", "MeasurementType",
    "CableInfo", "Folder", "ServiceLocation", "Asset",
    "Meter", "UsagePoint", "Department", "OperationalAuthority",
    "GeographicalRegion", "SubGeographicalRegion", "Plant",
    "ThermalGeneratingUnit", "HydroPowerPlant", "ControlArea",
    "AreaOfResponsibility", "CommunicationLink", "WeatherStation",
}

def local_name(tag):
    return tag.split("}")[-1]

def inspect_samples(filename):
    counts = defaultdict(int)
    lengths = defaultdict(list)
    stack = []

    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == "start":
            stack.append(local_name(elem.tag))
            continue

        if local_name(elem.tag) == "IdentifiedObject.name" and len(stack) >= 2:
            object_type = stack[-2]

            if object_type in TARGET_CLASSES:
                value = (elem.text or "").strip()
                if value:
                    counts[object_type] += 1
                    lengths[object_type].append(len(value))

        stack.pop()
        elem.clear()

    print("СТАТИСТИКА НАЗВАНИЙ (без исходного текста):")

    for object_type in sorted(counts):
        values = lengths[object_type]
        print(
            f"{object_type}: "
            f"объектов={counts[object_type]}, "
            f"мин. длина={min(values)}, "
            f"макс. длина={max(values)}"
        )

if __name__ == "__main__":
    inspect_samples(INPUT_FILE)
