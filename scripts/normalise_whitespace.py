# List of Files
FILES = ["1609.xml", "1623.xml"]

import xml.etree.ElementTree as ET

def main():
    for fileName in FILES:
        print(fileName)
        with open(fileName, "r", encoding="utf-8") as f:
            xml_data = f.read()
            canonical_data = ET.canonicalize(xml_data)  # Normalize whitespace
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(canonical_data)


if __name__ == "__main__":
    main()