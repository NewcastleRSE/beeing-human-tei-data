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

def get_ancestors(element, parent_map):
    ancestors = []
    while element in parent_map:
        element = parent_map[element]
        ancestors.append(element)
    return ancestors

def identify_common_ancestor(list_ancestors1, list_ancestors2):
    common_ancestor = None
    for ancestor in list_ancestors1:
        if ancestor in list_ancestors2:
            common_ancestor = ancestor
            break
    return common_ancestor

def find_common_ancestor(tree, element1, element2, ns, mapParent):
    # There will always be a common ancestor, and if both IDs exist, it's sort of pointless to error check here
    # Testing with anchors outside the root, and direct children of the root, there is no infinite loop -- it breaks on errors
    try:
        el1 = tree.find(f'.//TEI:anchor[@xml:id="{element1}"]', ns)
        el2 = tree.find(f'.//TEI:anchor[@xml:id="{element2}"]', ns)
    except KeyError:
        raise

    # makes a list of all ancestors for each element
    ancestors1 = get_ancestors(el1, mapParent)
    ancestors2 = get_ancestors(el2, mapParent)

    common_ancestor = identify_common_ancestor(ancestors1, ancestors2)

    return common_ancestor

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

def transform_editorial_notes_anchors_into_spans(tree, ns):
    # Auxiliary function used to gather editorial notes that need to be attached to the text via anchors rather than simply using a ref (necessary when the attachment point straddles different hierarchies). The function finds all the starting anchors, and for each one, finds the corresponding end anchor. For each start/end pair, it makes a list of all elements in between, then for each element in that list, it tries to determine its outermost element, where it applies a seg.
    
    # build a parent map for the tree
    parent_map = {c: p for p in tree.iter() for c in p}
    # find all the anchors that have a type='attachmentEditorialNote' and subtype="start"
    start_anchors = tree.findall(".//TEI:anchor[@type='attachmentEditorialNote'][@subtype='start']", ns)
    for start_anchor in start_anchors:
        # find the corresponding end anchor with subtype='end' and the same value of corresp as start_anchor
        end_anchor = tree.find(f".//TEI:anchor[@type='attachmentEditorialNote'][@subtype='end'][@corresp='{start_anchor.attrib['corresp']}']", ns)
        
        # find the common ancestor of the two anchors
        try: 
            common_ancestor = find_common_ancestor(tree, start_anchor.get(f'\u007b{ns["xml"]}\u007did'), end_anchor.get(f'\u007b{ns["xml"]}\u007did'), ns, parent_map)
        except KeyError:
            raise

        # go through every element in the parent ancestor and figure out what elements need to be collected
        collect = False
        tags = []
        for el in common_ancestor.iter():
            if el.get(f'\u007b{ns["xml"]}\u007did') == start_anchor.get(f'\u007b{ns["xml"]}\u007did'):
                collect = True
            if el.get(f'\u007b{ns["xml"]}\u007did') == end_anchor.get(f'\u007b{ns["xml"]}\u007did'):
                collect = False
            if collect:
                tags.append(el)

        deepTags = [];
        processedTags = [];
        endTagProcessed = False

        attributes = {'type': 'fragmentedNoteAttachement' ,'corresp': start_anchor.attrib['corresp']}

        for i, tag in enumerate(tags):
            if i == 0:
                span = ET.Element('seg', {**attributes, 'part': 'I'})
                    # collect the tail if it exists, then remove it
                if (tag.tail):
                    span.text = tag.tail
                    tag.tail = ''
                
                # Find if any of the following tags have the same parent as the starting element
                remainingTags = tags[i+1:]
                siblingTags = []
                for i, innerTag in enumerate(remainingTags):
                    if parent_map[innerTag] == parent_map[start_anchor]:
                        siblingTags.append(innerTag)
                
                # for each of the sibling tags, find which elements in tags are their descendants
                for siblingTag in siblingTags:
                    # find the index of the siblingTag in tags
                    index = tags.index(siblingTag)
                    # find the descendants of the siblingTag
                    for innerTag in tags[index:]:
                        if innerTag in siblingTag.iter():
                            deepTags.append(innerTag)
                
                # add each of the siblings to the span
                for siblingTag in siblingTags:
                    span.append(siblingTag);
                    processedTags.append(siblingTag)
                    # remove the sibling tags from their parent
                    parent_map[siblingTag].remove(siblingTag);

                # insert the span right after the start_anchor
                for i, element in enumerate(parent_map[start_anchor]):
                    if element == start_anchor:
                        parent_map[start_anchor].insert(i+1, span)
                        break
            else:
                # check to see if the end_anchor is a descendant of the tag
                if end_anchor in tag.iter():
                    # checks to see if the end_anchor is a direct child of the tag
                    if parent_map[end_anchor] != tag:
                        # if the end_anchor is not a direct child of the tag, find the direct child of the tag that is an ancestor of the end_anchor
                        direct_child = parent_map[end_anchor]
                        while parent_map[direct_child] != tag:
                            direct_child = parent_map[direct_child]
                        print(direct_child)

                        # create a new span that will take everything from the start of tag to the direct child
                        new_span = ET.Element('seg', {**attributes, 'part': 'M'})
                        # if there is any text between the start of the tag and the direct child, collect that
                        if tag.text and not tag.text.isspace():
                            new_span.text = tag.text
                            tag.text = ''
                        toRemove = []
                        for el in tag.iter():
                            if el == direct_child:
                                break
                            elif el != tag and parent_map[el] == tag:
                                new_span.append(el)
                                toRemove.append(el)
                            elif el != tag and parent_map[el] != tag:
                                deepTags.append(el)
                            
                        # if the new_span has no children, and no text or tail, can be ignored
                        if len(new_span) != 0 or new_span.text or new_span.tail:
                            # insert the new span at the start of the tag
                            tag.insert(0, new_span)
                        # remove the elements that have been moved
                        for el in toRemove:
                            if el in tag.iter():
                                tag.remove(el)
                        
                        endTagProcessed = True
                    else:
                        span = ET.Element('seg', {**attributes, 'part': 'F'})
                        toRemove = [];
                        for el in tag.iter():
                            if el != tag:
                                # if el is not the end anchor but is a sibling of end anchor, add it to the span
                                if el != end_anchor and parent_map[el] == parent_map[end_anchor]:
                                    span.append(el)
                                    toRemove.append(el)
                                elif (el == end_anchor):
                                    break
                        if tag.text:
                            span.text = tag.text
                            tag.text = ''
                        # insert the span at the start of the tag
                        tag.insert(0, span);
                        # remove the elements that have been move
                        for el in toRemove:
                            if el in tag.iter():
                                tag.remove(el)
                        endTagProcessed = True
                else:
                    # if not, the entire content of the tag should become a child of a new seg element, but only if the endTag has not been processed (i.e., tags after that will have been descendents of the last parent of the endTag)
                    if not endTagProcessed and (tag not in deepTags) and (tag not in processedTags):

                        # checks to see which of the other tags might be children of the current tag
                        remainingTags = tags[i:]
                        for i, innerTag in enumerate(remainingTags):
                            if innerTag in tag.iter() and i > 0:
                                deepTags.append(innerTag)
                        
                        new_span = ET.Element('seg', {**attributes, 'part': 'M'})

                        # If there is any text between the start of the tag and its first child, collect that
                        if tag.text:
                            new_span.text = tag.text
                            tag.text = '';
                        
                        toRemove = []
                        
                        for el in tag.iter():
                            if el != tag and parent_map[el] == tag:
                                new_span.append(el)
                                toRemove.append(el)

                        for el in toRemove:
                            if el in tag.iter():
                                tag.remove(el)

                        # add the new span to the tag
                        tag.insert(0, new_span)

                        # if the tag has a tail and its parent is not part of the tag list (meaning it's parent contains the start anchor), create a new span for the tail
                        if tag.tail and parent_map[tag] not in tags:
                            # if tag.tail only contains whitespace, ignore it
                            if not tag.tail.isspace():
                                print('Tail being considered')
                                tail_span = ET.Element('seg', {**attributes, 'part': 'M'})
                                tail_span.text = tag.tail
                                tag.tail = ''
                                # place the new span after the tag
                                for i, element in enumerate(parent_map[tag]):
                                    if element == tag:
                                        parent_map[tag].insert(i+1, tail_span)
                        
        
  
       


def append_hi_summary_notes(tree, ns): 
    # marginal notes
    sum_notes = tree.findall(".//TEI:note[@subtype='summary']", ns)
    for el in sum_notes:
        correctEl = None
        text = None
        # Checks if element contains text and is not all whitespace
        if el.text and not el.text.isspace():
            correctEl = el
        elif len(el.findall('.//TEI:lem', ns)) > 0:
            # note contains app, need to find the lem
            correctEl = el.find('.//TEI:lem', ns)
            print(el.find('.//TEI:lem', ns).text)
        else:
            # note contains only a single element that should have its own rendering information
            correctEl = None
            text = ''
            
        if correctEl != None:
            # removing any unecessary whitespace characters
            text = " ".join(correctEl.text.split())
            # add a trailing space to account for elements inside notes
            text += " "
            text = text.split('. ', 1)

        if text != None and len(text) > 1 and correctEl != None:
            correctEl.text = f'{text[0]}. '
            italicsEl = ET.SubElement(correctEl, 'seg', {'rend': 'italic'})
            italicsEl.text = text[1]
            # find out if the note element has children (i.e.,  a <term> for example)
            if len([elem.tag for elem in correctEl.iter() if elem is not correctEl and elem is not italicsEl]) > 0:
                toRemove = []
                # places elements in the correct order
                for child in correctEl:
                    if child is not italicsEl:
                        toRemove.append(child.tag)
                        italicsEl.append(child)
                # removes elements that have been moved
                for tag in toRemove:
                    for el in correctEl.findall(tag):
                        correctEl.remove(el)                        
            # checks if there are any digits in the note text, if there are, does character by character formatting
            if (any(char.isdigit() for char in italicsEl.text)):
                text = italicsEl.text
                italicsEl.text = ''
                if text:
                    for char in text:
                        if char.isdigit():
                            digitEl = ET.SubElement(italicsEl, 'seg', {'rend': 'normal'})
                            digitEl.text = char
                        else:
                            alphaEl = ET.SubElement(italicsEl, 'seg', {'rend': 'italic'})
                            alphaEl.text = char
    # refs
    refs = tree.findall(".//TEI:ref", ns)
    for el in refs:
        el.text
        text = el.text
        if text:
            # find out if the ref element has children (i.e.,  a <term> for example)
            if len([elem.tag for elem in el.iter() if elem is not el]) > 0:
                # Elements like this will be hardcoded
                # print('I affect ' , el.text);
                continue
            else:
                # default behaviour: each character is formatted individually
                el.text = ''
                for char in text:
                    if char.isdigit():
                        digitEl = ET.SubElement(el, 'seg', {'rend': 'normal'})
                        digitEl.text = char
                    else:
                        alphaEl = ET.SubElement(el, 'seg', {'rend': 'italic'})
                        alphaEl.text = char

def main(preview=False):
    import sys, os

    FILEOUTPUT = '1623_consolidated.xml'

    if (preview):
        FILEOUTPUT = 'preview/preview_1623_consolidated.xml'
        
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
    
    # add hi to all the summary notes in the correct places
    # need to do error catching for this function
    append_hi_summary_notes(tree, ns)
    transform_editorial_notes_anchors_into_spans(tree, ns)

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