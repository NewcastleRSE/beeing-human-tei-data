def find_all_html_entitites(data):
    # find all the html entities
    import re
    html_entities = re.finditer(r'&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});', data, flags=re.IGNORECASE)
    forbidden_indices = []
    for entity in html_entities:
        # for each entity, find its index in the data
        forbidden_indices.append(entity.end() - 1)
    return forbidden_indices

def replace_semicolon(data, forbidden_indices):
    consolidated_data = ""
    for i in range(len(data)):
        if data[i] == ";":
            if i in forbidden_indices:
                print(i)
                consolidated_data += ";"
            else:
                consolidated_data += "<seg rend='roman'>;</seg>"
        else:
            consolidated_data += data[i]
    return consolidated_data

def main():
    # load the file
    with open("1623_consolidated.xml", "r") as f:
        data = f.read()
        forbidden_indices = find_all_html_entitites(data)
        updated_data = replace_semicolon(data, forbidden_indices)
        # write the updated data to a new file
    with open("1623_consolidated_semicolon.xml", "w") as f:
        f.write(updated_data)
    
        

if __name__ == "__main__":
    main()