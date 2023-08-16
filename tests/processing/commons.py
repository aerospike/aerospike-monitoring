import json

#takes the file name as input,extracts all the data from the file,uses parse_queries_to_dict to convert it into a dictionary and then returns the dictionary.
def read_dashboard_queries(p_filename):
    dict_queries = {}
    queries = open( p_filename, "r")  
    for query in queries:
        entry = json.loads(query)
        key = entry['key']  # Use the 'key' field from the entry as the dictionary key
        dict_queries[key] = entry['entry']  # Store the 'entry' dictionary as a value

    return dict_queries

#takes input dictionary and list of ordered keys,searches for the the values in the dictinary 
#and constructs a key based on thes key and their order
def construct_key(p_entry_dict, p_key_names):
    l_key_made = ""
    for k in p_key_names:
        l_key_made = l_key_made + "/" + p_entry_dict[k]
    return l_key_made

#takes input,constructs a key,and uses this to make set of keys for counting purposes
def loop_for_count(p_which_dict,p_key_array):
    l_SET_DICT = set()
    for line in p_which_dict:
        entry = p_which_dict[line]
        key = construct_key(entry,p_key_array)
        l_SET_DICT.add(key)
    return l_SET_DICT

#takes input,then constructs a dictionary with the input
def loop_for_names(p_which_dict,p_key_array,p_entry_element):
    l_SET_DICT = {}
    for line in p_which_dict:
        entry = p_which_dict[line]
        key = construct_key(entry,p_key_array)

        if key in l_SET_DICT:
            if entry[p_entry_element] not in l_SET_DICT[key]:
                updated_tuple = l_SET_DICT[key] + (entry[p_entry_element],)
                l_SET_DICT[key] = updated_tuple
        else:
            l_SET_DICT[key] = (entry[p_entry_element],)
    return l_SET_DICT

#takes input dictionaries and compares them in A - B format and returns the result.the answer depends on order of input dictionaries
def loop_for_comparision( p_Dict_A, p_Dict_B):
    SET_A_minus_B = {}
    for key in p_Dict_A:
        if key in p_Dict_B:
            value_tuple = tuple(set(p_Dict_A[key]) - set(p_Dict_B[key]))
            if value_tuple:
                SET_A_minus_B[key] = value_tuple
        else:
            SET_A_minus_B[key] = p_Dict_A[key]
    return SET_A_minus_B
