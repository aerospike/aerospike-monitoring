import json

def process_value(value, second_data_lines):
    if isinstance(value, dict):
        new_dict = {}
        for k, v in value.items():
            new_dict[k] = process_value(v, second_data_lines)
        return new_dict
    elif isinstance(value, list):
        new_list = []
        for item in value:
            new_list.append(process_value(item, second_data_lines))
        return new_list
    else:
        for line in second_data_lines:
            #print(line.strip().startswith(value))
            #print(value)
            print(line)
            #print("cluster_aerospike: \"dshad\"".startswith(value + ':'))
            #print(line.startswith(value + ':'))
            if line.strip().startswith(value + ':'):
                #print(line.strip(':'))
                _, found_value = line.split(':', 1)
                #print(found_value)
                return found_value.strip()
        return '"not_available"'

def process_first_file(first_data, second_data_lines):
    third_data = process_value(first_data, second_data_lines)
    return third_data

def write_third_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    first_filename = 'alert_config_data.json'
    second_filename = 'defaults.yaml'
    third_filename = 'new.json'

    with open(first_filename, 'r') as file:
        first_data = json.load(file)
    with open(second_filename, 'r') as file:
        second_data_lines = file.readlines()

    third_data = process_first_file(first_data, second_data_lines)

    write_third_file(third_data, third_filename)

if __name__ == "__main__":
    main()