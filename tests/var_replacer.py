import json

def load_replacements(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

def get_dashboard_name(line):
    return line.split("/")[0]

def apply_replacements(replacements, text_content):
    lines = text_content.split("\n")
    updated_lines = []

    for line in lines:
        dashboard_name = get_dashboard_name(line)
        if dashboard_name in replacements:
            for placeholder, replacement in replacements[dashboard_name].items():
                line = line.replace(placeholder, replacement)
        updated_lines.append(line)

    return "\n".join(updated_lines)

def main():
    replacements_file = "test_variables.json"
    text_file = "a.txt"
    output_file = "b.txt"

    # Load replacements from JSON file
    replacements = load_replacements(replacements_file)

    # Read the content from the text file
    with open(text_file, "r") as file:
        text_content = file.read()

    # Apply replacements
    updated_content = apply_replacements(replacements, text_content)

    # Save the updated content to a new file
    with open(output_file, "w") as file:
        file.write(updated_content)

    print("Replacements applied successfully. Updated content saved to:", output_file)

if __name__ == "__main__":
    main()