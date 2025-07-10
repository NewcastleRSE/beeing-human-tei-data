import xml.etree.ElementTree as ET

def main():
    # Define namespaces dictionary to navigate the tree
    ns = {
        'TEI': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }

    with open("data-analysis/cross-refs.csv", "w", encoding="utf-8") as out_file:
        out_file.write("source,target,destination\n")

    with open("1623.xml", "r", encoding="utf-8") as f:
        xml_data = f.read()
        root = ET.fromstring(xml_data)

        # find all divs type chapter
        chapters = root.findall(".//TEI:div[@type='chapter']", namespaces=ns)

        # add div with id="preface" to the list of chapters
        preface = root.find(".//TEI:div[@type='preface']", namespaces=ns)
        if preface is not None:
            chapters.insert(0, preface)

        # for each chapter, get a list of all the refs that have a target element

        for chapter in chapters:
            refs = chapter.findall(".//TEI:ref[@target]", namespaces=ns)

            # exclude all the refs whose target does not start with #
            refs = [ref for ref in refs if ref.get("target", "").startswith("#")]

            # print all refs
            for ref in refs:
                target = ref.get("target")
                source = f'ch{chapter.get("n")}'
                if target:
                    # if target contains 'sumn'
                    if "sumn" in target:
                        destination = target.split("#")[-1]
                        # extracts chapter number from destination which will be the start of the string until the first non-digit character following the ch
                        if destination.startswith("ch") and len(destination) > 3:
                            
                            if destination[3].isdigit():
                                destination = destination[:4]
                            else:
                                destination = destination[:3]
                    
                    
                        # write the results to an output csv file
                        with open("data-analysis/cross-refs.csv", "a", encoding="utf-8") as out_file:
                            out_file.write(f'{source},{target},{destination}\n')
                        
            if len(refs) == 0:
                print("No refs found with target attribute.")
            print(f'{chapter.get("n")}: {len(refs)} refs found with target attribute.')

if __name__ == "__main__":
    main()