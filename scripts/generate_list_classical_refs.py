import xml.etree.ElementTree as ET

def process_file(xml_filename, output_csv):
    ns = {
        'TEI': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }

    abbr = {
        'aristom.': 'aristomachus',
        'aristotles': 'aristotle',
        'orythia': 'orithya',
        'pliny': 'plinie',
        'plinie,': 'plinie',
        'plinie.': 'plinie',
        'var.': 'varro',
        'columella.': 'columella',
        'columella,': 'columella',
        'plin.': 'plinie',
        'raymond lulli': 'raimundus lullius',
        'plato,': 'plato'
    }

    with open(output_csv, "w", encoding="utf-8") as out_file:
        out_file.write("source,destination\n")

    with open(xml_filename, "r", encoding="utf-8") as f:
        xml_data = f.read()
        root = ET.fromstring(xml_data)

        chapters = root.findall(".//TEI:div[@type='chapter']", namespaces=ns)
        preface = root.find(".//TEI:div[@type='preface']", namespaces=ns)
        if preface is not None:
            chapters.insert(0, preface)

        classical_authors = [];

        for chapter in chapters:
            people = chapter.findall(".//TEI:persName", namespaces=ns)

            # for person in people:
            for person in people:
                # get the content of the persName element
                person_name = person.text.strip() if person.text else ""
                # if person_name exists, remove any extra whitespace and add it to the CSV
                if person_name:
                    person_name = " ".join(person_name.split())
                    # add it to the array of classical authors
                    classical_authors.append(person_name)
        
        for author in classical_authors:
            # normalize the spelling of the author name
            author = author.lower()
            # if the author is in the abbreviation dictionary, replace it
            if author in abbr:
                author = abbr[author]
            # write the author to the CSV file
            with open(output_csv, "a", encoding="utf-8") as out_file:
                out_file.write(f'butler,{author}\n')

def main():
    process_file("1623.xml", "data-analysis/classical-refs-1623.csv")
    process_file("1609.xml", "data-analysis/classical-refs-1609.csv")

if __name__ == "__main__":
    main()