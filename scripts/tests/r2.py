import json

def process_value(json_templ_file, second_data_lines):

    second_dict = {}    
    for line in second_data_lines:
        line = line.strip()        
        if len(line)>0 and ":" in line and not line.startswith("#") :
            elements = line.split(":")
            key = elements[0]
            second_dict[ key]= elements[1].strip().replace(" ","")

    for key in json_templ_file.keys():
        if "list" not in str(type(json_templ_file[key])) :
            if key in second_dict:
                json_templ_file[ key]= second_dict[ key]
            else:
                json_templ_file[ key]= "not-available"
                    
def process_first_file(first_data, second_data_lines):
    third_data = process_value(first_data, second_data_lines)
    return third_data

def write_third_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    first_filename = '/Users/phaniram/dirtywork/prom_docker/tests/alert_config_data.json'
    second_filename = '/Users/phaniram/dirtywork/prom_docker/tests/defaults.yaml'
    third_filename = 'new.json'

    with open(first_filename, 'r') as file:
        first_data = json.load(file)
    with open(second_filename, 'r') as file:
        second_data_lines = file.readlines()

    third_data = process_first_file(first_data, second_data_lines)

    # write_third_file(third_data, third_filename)

if __name__ == "__main__":
    main()