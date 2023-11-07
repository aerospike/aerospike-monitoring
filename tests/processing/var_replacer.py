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
    error_messages = set()
    list_of_variables = ["$set_quota_topk" ,"$node", "$severity", "$state", "$job_name", "$cluster", "$namespace", "$set", 
                         "$sindex", "$dc", "${operation}", "$latency_time_bucket", "$job_id", "$operation",
                         "$xdr_proxy_cluster_name", "$kafka_cluster_name", "$pulsar_cluster_name", 
                         "$jms_cluster_name", "$elastic_cluster_name", "$esp_cluster_name", "$instance", "$connector_type", 
                         "$user", "${latencytimeunit}", "$__rate_interval", "$topk_limit"]

    for line in lines:
        dashboard_name = get_dashboard_name(line)

        # encode every " with \" for query execution
        # line = line.replace('"', '\'')
        # print( line)
        if dashboard_name in replacements:
            # for placeholder, replacement in replacements[dashboard_name].items():
            for l_variable in list_of_variables:
                replacement = fetch_replacement_value( dashboard_name, replacements, l_variable)
                # promql variable can be like $node or $node|$^
                line = line.replace("|$^", "")
                line = line.replace(":pipe", "")
                line = line.replace(l_variable, replacement)
        else:
            error_messages.add ("dashboard: "+dashboard_name +" no over-rides, using default_for_all values")
            for placeholder, replacement in replacements["default_for_all"].items():
                # promql variable can be like $node or $node|$^
                line = line.replace("|$^", "")
                line = line.replace(":pipe", "")
                line = line.replace(placeholder, replacement)
                # print(line)
            
        updated_lines.append(line)
    print(error_messages)
    return "\n".join(updated_lines)

def fetch_replacement_value( p_dashboard_name, p_replacements, p_variable):
    for placeholder, replacement in p_replacements[p_dashboard_name].items():
        if placeholder == p_variable:
            return replacement
    # return default 
    for placeholder, replacement in p_replacements["default_for_all"].items():
        if placeholder == p_variable:
            return replacement
        
    return p_variable

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
    