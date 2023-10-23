import xml.etree.ElementTree as ET

tree = ET.parse('./1623.xml')
root = tree.getroot()

print(root);