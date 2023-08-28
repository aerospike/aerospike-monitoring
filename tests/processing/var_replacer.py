import json

from globals import fn_mock_variables, fn_fullform_queries, fn_mock_queries

def load_replacements(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

def get_dashboard_name(line):
    parts = line.split("/")
    for ele in parts:
        if ele.endswith(".json"):
            return ele

    return ""

def apply_replacements(replacements, text_content):
    lines = text_content.split("\n")
    updated_lines = []

    for line in lines:
        dashboard_name = get_dashboard_name(line)

        # encode every " with \" for query execution
        # line = line.replace('"', '\'')
        # print( line)
        
        if dashboard_name in replacements:
            for placeholder, replacement in replacements[dashboard_name].items():
                line = line.replace(placeholder, replacement)
        updated_lines.append(line)

    return "\n".join(updated_lines)

def replace_variable():

    # Load replacements from JSON file
    replacements = load_replacements(fn_mock_variables)

    # Read the content from the text file
    with open(fn_mock_queries, "r") as file:
        text_content = file.read()

    # Apply replacements
    updated_content = apply_replacements(replacements, text_content)

    # Save the updated content to a new file
    with open( fn_fullform_queries, "w") as file:
        file.write(updated_content)

    print("Replacements applied successfully. Updated content saved to:", fn_fullform_queries)

if __name__ == "__main__":
    replace_variable()
    