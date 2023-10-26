# File names
FILE1623 = "1623_example.xml"
FILE1609 = "1609_example.xml"

# Error Return Codes
ERROR = 0

import xml.etree.ElementTree as ET


def buildParentMap():
    try:
        tree = ET.parse(FILE1609)
        parent_map = {c: p for p in tree.iter() for c in p}
        return parent_map, tree
    except FileNotFoundError:
        raise

def find_common_ancestor(tree, element1, element2, ns, mapParent):
    el1 = tree.find(f'.//TEI:anchor[@xml:id="{element1}"]', ns)
    el2 = tree.find(f'.//TEI:anchor[@xml:id="{element2}"]', ns)
    if mapParent[el1] == mapParent[el2]:
        return mapParent[el1]
    else:
        return _find_common_ancestor(mapParent[el1], mapParent[el2], mapParent)
        

def _find_common_ancestor(element1, element2, mapParent):
    if mapParent[element1] == mapParent[element2]:
        return mapParent[element1]
    else:
        return _find_common_ancestor(mapParent[element1], mapParent[element2], mapParent)

def getText(string, ns, mapParent, tree):
    # get two targets
    start_end = string.split()
    if len(start_end) != 2:
        raise ValueError(f'Error: Expected two xml:id, instead this was found: "{string}"')

    # isolate xml:id and build full anchor
    for i, id in enumerate(start_end):
        start_end[i] = id.split("#")[1]

    # Ensure both ids exist in 1609
    for id in start_end:
        if tree.find(f'.//TEI:anchor[@xml:id="{id}"]', ns) == None:
            raise ValueError(f'Error: xml:id="{id}" does not exist in "{FILE1609}"')

    # Find the earliest common ancestor
    parent = find_common_ancestor(tree, start_end[0], start_end[1], ns, mapParent)
    collect = False
    tags = []
    
    # Go through every element in the ancestor and figure out what elements need to be collected
    for el in parent.iter():
        if el.get(f'\u007b{ns["xml"]}\u007did') == start_end[0]:
            collect = True
        if el.get(f'\u007b{ns["xml"]}\u007did') == start_end[1]:
            collect = False
        if collect:
            tags.append(el)
    text = ""

    # Go through every collected element and collect text
    for tag in tags:
        # Text only includes inner text until the next tag (which is convienient for me). See:
        # https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.text
        if tag.text:
            text += ''.join([tag.text, tag.tail])
            # find a way to preserve inner elements
            # text += ''.join([f'<{tag.tag}>', tag.text, f'</{tag.tag}>', tag.tail])
        else:
            text += tag.tail

        
    return text
    
def main():

    # Define namespaces dictionary to navigate the tree
    ns = {
        'TEI': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }

    # Load the 1623
    try:
        tree = ET.parse(FILE1623)
    except FileNotFoundError as e:
        print(e)
        return ERROR

    # Find elements
    # selects the parent (..) of all ptr inside rdg (i.e., selects rdg)
    try:
        rdgs = tree.findall(".//TEI:rdg/TEI:ptr/..", ns)
        if rdgs == []:
            raise ValueError(f'Error: There is no apparatus in "{FILE1623}"')
    except ValueError as e:
        print(e)
        return ERROR

    # Built parent map and tree for 1609
    try:
        mapParent1609, tree1609 = buildParentMap()
    except FileNotFoundError as e:
        print(e)
        return ERROR

    for rdg in rdgs:
        # Find target
        ptr = rdg.find('TEI:ptr', ns) # No need to error check this one, rdgs will always contain ptr (see findall above)
        target = ptr.attrib['target']
        
        try:
            # Get text from 1609
            newText = getText(target, ns, mapParent1609, tree1609)
        
            # Record target information in the rdg
            rdg.attrib['source'] = target

            # Replace ptr with text from 1609
            rdg.remove(ptr)
            rdg.text = newText
        except ValueError as e:
            print(e)

    # To write results
    ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
    tree.write("test_output.xml")

if __name__ == "__main__":
    main()