def getText(string):
    import re

    # get two targets
    start_end = string.split()

    # get file name
    fileName = start_end[0].split('#')[0]

    # isolate xml:id and build full anchor
    for i, id in enumerate(start_end):
        start_end[i] = f'<anchor xml:id=\"{id.split("#")[1]}\"/>'


    # open file
    with open(fileName, 'r') as file:
        text = file.read()
        # NEED TO REMOVE ANY POSSIBLE EMPTY SPACES BETWEEN THE END OF THE XML:ID AND CLOSING THE TAG
        # ALTERNATIVELY FIND A WAY OF EXTRACTING TEXT BEWEEN TWO TAGS
        # find substring
        result = re.search(f'{start_end[0]}(.*){start_end[1]}', text).group(1)
        print(result)


    return result
    

import xml.etree.ElementTree as ET

ns = {
    'TEI': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

# Load the document
tree = ET.parse('./1623_example.xml')
root = tree.getroot()


# Find elements
# selects the parent (..) of all ptr inside rdg (i.e., selects rdg)
rdgs = tree.findall("//TEI:rdg/TEI:ptr/..", ns)

for rdg in rdgs:
    # Find target
    ptr = rdg.find('TEI:ptr', ns)

    # Record target information in the rdg
    target = ptr.attrib['target']
    rdg.attrib['source'] = target

    # Get text from 1609
    newText = getText(target)

    # Replace ptr with text from 1609
    rdg.remove(ptr)
    rdg.text = newText

# To write results
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
tree.write("test_output.xml")