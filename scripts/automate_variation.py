def getText(string, ns):
    import re, os
    import xml.etree.ElementTree as ET

    # get two targets
    start_end = string.split()

    # get file name
    fileName = start_end[0].split('#')[0]

    # isolate xml:id and build full anchor
    for i, id in enumerate(start_end):
        # start_end[i] = f'<anchor xml:id=\"{id.split("#")[1]}\"/>'
        start_end[i] = id.split("#")[1]

    tree = ET.parse(fileName)

    parent = tree.find(f'.//TEI:anchor[@xml:id="{start_end[0]}"]/..', ns)
    collect = False
    tags = []
    for el in parent.iter():
        if el.get(f'\u007b{ns["xml"]}\u007did') == start_end[0]:
            collect = True
        if el.get(f'\u007b{ns["xml"]}\u007did') == start_end[1]:
            collect = False
        if collect:
            tags.append(el)
    text = ""
    for tag in tags:
        if tag.text:
            text += ''.join([tag.text, tag.tail])
        else:
            text += tag.tail
    print(text)
    print ("+++++++++++++")

        
    # open file
    # with open(fileName, 'r', encoding='utf-8') as file:
    #     text = file.read()
        # NEED TO REMOVE ANY POSSIBLE EMPTY SPACES BETWEEN THE END OF THE XML:ID AND CLOSING THE TAG
        # ALTERNATIVELY FIND A WAY OF EXTRACTING TEXT BEWEEN TWO TAGS
        # find substring
        # result = re.search(f'{start_end[0]}(.*){start_end[1]}', text).group(1)
        # print(result)



    return 'NOTHING'
    

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
rdgs = tree.findall(".//TEI:rdg/TEI:ptr/..", ns)

for rdg in rdgs:
    # Find target
    ptr = rdg.find('TEI:ptr', ns)

    # Record target information in the rdg
    target = ptr.attrib['target']
    rdg.attrib['source'] = target

    # Get text from 1609
    newText = getText(target, ns)

    # Replace ptr with text from 1609
    rdg.remove(ptr)
    rdg.text = newText

# To write results
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
tree.write("test_output.xml")