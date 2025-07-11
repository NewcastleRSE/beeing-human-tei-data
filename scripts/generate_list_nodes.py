import xml.etree.ElementTree as ET

def process_file(xml_filename, output_csv, edition_label):
    ns = {
        'TEI': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }

    with open(output_csv, "w", encoding="utf-8") as out_file:
        out_file.write("source,target,destination\n")

    with open(xml_filename, "r", encoding="utf-8") as f:
        xml_data = f.read()
        root = ET.fromstring(xml_data)

        chapters = root.findall(".//TEI:div[@type='chapter']", namespaces=ns)
        preface = root.find(".//TEI:div[@type='preface']", namespaces=ns)
        if preface is not None:
            chapters.insert(0, preface)

        for chapter in chapters:
            refs = chapter.findall(".//TEI:ref[@target]", namespaces=ns)
            refs = [ref for ref in refs if ref.get("target", "").startswith("#")]

            for ref in refs:
                target = ref.get("target")
                if chapter.get("n") is None and chapter.get('type') == 'preface':
                    source = 'preface'
                else:
                    source = f'ch{chapter.get("n")}'
                if target:
                    if "sumn" in target:
                        destination = target.split("#")[-1]
                        if destination.startswith("ch") and len(destination) > 3:
                            if destination[3].isdigit():
                                destination = destination[:4]
                            else:
                                destination = destination[:3]
                        with open(output_csv, "a", encoding="utf-8") as out_file:
                            out_file.write(f'{source},{target},{destination}\n')
            if len(refs) == 0:
                print(f"[{edition_label}] No refs found with target attribute.")
            print(f'[{edition_label}] {source}: {len(refs)} refs found with target attribute.')

def main():
    process_file("1623.xml", "data-analysis/cross-refs-1623.csv", "1623")
    process_file("1609.xml", "data-analysis/cross-refs-1609.csv", "1609")

if __name__ == "__main__":
    main()