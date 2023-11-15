# File names
FILE1623 = "1623.xml"
FILE1609 = "1609.xml"
# FILE OUTPUT DEFINED IN MAIN()

# Error Return Codes
ERROR = 10
SUCCESS = 0

import xml.etree.ElementTree as ET


def buildParentMap():
    try:
        tree = ET.parse(FILE1609)
        parent_map = {c: p for p in tree.iter() for c in p}
        return parent_map, tree
    except FileNotFoundError:
        raise

def find_common_ancestor(tree, element1, element2, ns, mapParent):
    # There will always be a common ancestor, and if both IDs exist, it's sort of pointless to error check here
    # Testing with anchors outside the root, and direct children of the root, there is no infinite loop -- it breaks on errors
    try:
        el1 = tree.find(f'.//TEI:anchor[@xml:id="{element1}"]', ns)
        el2 = tree.find(f'.//TEI:anchor[@xml:id="{element2}"]', ns)
    except KeyError:
        raise
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
    try:
        parent = find_common_ancestor(tree, start_end[0], start_end[1], ns, mapParent)
    except KeyError:
        # If the recursion reaches the end of the tree it will throw a key error
        raise
    
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
    for i, tag in enumerate(tags):
        # Text only includes inner text until the next tag (which is convienient for me). See:
        # https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.text
        try:
            if tag.text:
                if tag.tail:
                    text += ''.join([tag.text, tag.tail])
                else:
                    text += tag.text
                # find a way to preserve inner elements
                # text += ''.join([f'<{tag.tag}>', tag.text, f'</{tag.tag}>', tag.tail])
            elif tag.tail:
                text += tag.tail
            elif i < len(tag):
                # falls into this case if the anchor starts with an element
                # if it's not the last, keep going
                pass
        except:
            print(f'ERROR: Something went wrong collecting the text: check between {start_end[0]} and {start_end[1]} in 1609.xml')        
    return text

def append_XML_dec(FILEOUTPUT):
    xml_dec = '<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="schema/tei_beeing_human.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="schema/tei_beeing_human.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n'

    with open(FILEOUTPUT, 'r') as file:
        # reads xml
        content = file.read()
    
    # adds declaration
    content = xml_dec + content

    with open(FILEOUTPUT, 'w') as file:
        # write content
        file.write(content)

def main(preview=False):
    import sys, os

    FILEOUTPUT = '1623_consolidated.xml'

    if (preview):
        FILEOUTPUT = 'preview_1623_consolidated.xml'
        
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
        sys.exit(ERROR)

    # Find elements
    # selects the parent (..) of all ptr inside rdg (i.e., selects rdg)
    try:
        rdgs = tree.findall(".//TEI:rdg/TEI:ptr/..", ns)
        if rdgs == []:
            app = tree.findall(".//TEI:rdg/TEI:app", ns)
            if app == []:
                print(f'Exiting: \'{FILE1623}\' contains no app elements.')
                return SUCCESS
            else:
                raise ValueError(f'Error: There is apparatus but no pointers in \'{FILE1623}\'')
    except ValueError as e:
        print(e)
        sys.exit(ERROR)

    # Built parent map and tree for 1609
    try:
        mapParent1609, tree1609 = buildParentMap()
    except FileNotFoundError as e:
        print(e)
        sys.exit(ERROR)

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
        except KeyError as e:
            print(f'Error: {target} points to elements that do not share a common ancestor')

    # removes any old versions of the file, in case no new one has been created during the run
    try:
        os.remove(FILEOUTPUT)
    except FileNotFoundError:
        print('No old consolidated file exists...')
    # To write results
    ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
    tree.write(FILEOUTPUT)

    try:
        append_XML_dec(FILEOUTPUT)
    except FileNotFoundError:
        print(f'Fatal error: Could not write the output to \'{FILEOUTPUT}\'')
        sys.exit(ERROR)
    print('Consolidation successful')
    return SUCCESS

if __name__ == "__main__":
    main()