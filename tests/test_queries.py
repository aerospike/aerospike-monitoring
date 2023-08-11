import requests

filename_baseline_queries = "mockdata/baseline_dashboard.queries"
filename_mock_queries = "mockdata/mock_dashboard.queries"

baseline_dict_queries = {}
mock_dict_queries = {}

def read_dashboard_queries(p_filename):
    dict_queries = {}
    fd_queries = open( p_filename, "r")   
    dict_queries = parse_queries_to_dict(fd_queries)
    return dict_queries

# end test-cases
def parse_queries_to_dict(queries):
    result = {}
    
    for query in queries:
        parts = query.strip().split(' = ')
        if len(parts) == 2:
            key = parts[0]
            value = parts[1].strip()  # Remove leading/trailing whitespace
            
            # Parsing key
            key_parts = key.split('/')
            if len(key_parts) >= 9:  
                folder = key_parts[0]
                dashboard_file = key_parts[1]
                dashboard_name = key_parts[2]
                row_title = key_parts[3]
                row_id = key_parts[4]
                panel_name = key_parts[5]  
                panel_id = key_parts[6]  
                refid = key_parts[7]  
                index = key_parts[8]  
                
                # Constructing dictionary entry
                entry = {
                    "folder": folder,
                    "dashboard_file": dashboard_file,
                    "dashboard_name": dashboard_name,
                    "row_title": row_title,
                    "row_id": row_id,
                    "panel_name": panel_name,
                    "panel_id": panel_id,
                    "refid": refid,
                    "index": index,
                    "expr": value
                }
                
                result[key] = entry
    
    return result
            
def compare_base_expr_with_latest(p_key):
    old_expr = baseline_dict_queries[p_key]["expr"]
    new_expr = mock_dict_queries[p_key]["expr"]
    #TODO:-construct assert message 
    assert old_expr == new_expr



def test_compare_exprs_in_dicts():
    for key in mock_dict_queries:
        if key in baseline_dict_queries:
            #print(old_expr)
            compare_base_expr_with_latest(key)




baseline_dict_queries = read_dashboard_queries(filename_baseline_queries)
mock_dict_queries = read_dashboard_queries(filename_mock_queries)


test_compare_exprs_in_dicts()