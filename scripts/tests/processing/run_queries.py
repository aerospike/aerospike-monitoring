import requests
import json
import os

DEFAULT_PROM_URL = "http://localhost:45880/api/v1/query"
prometheus_url_to_get = os.environ.get( "PROMETHEUS_URL" , DEFAULT_PROM_URL)

# list of dashboard-json-filenames, 
#   to process
g_dashboard_names = [ "home/alerts.json", "home/alertsview.json", "home/exporters.json", 
                      "home/geoview.json", "home/jobs.json", "home/latency.json",
                      "home/namespace.json", "home/node.json", 
                      "home/set.json", "home/sindex.json", "home/uniquedata.json", 
                      "home/users.json", "home/xdr.json", 
                      "usecases/all_flash.json", "usecases/rolling_restart.json",
                      "connectors/connectorsview.json", "connectors/connector_jvmview.json",
                     ]

# -- to ignore during executino
# this should be a LIMITED list
g_ignore_list_dashboards= ["home/uniquedata.json"]

# list of queries or query-key to ignore
# this should be a LIMITED list
g_ignore_list_queries= ["row no expression", "panel no expression"]

# output json file format
# <dashboard-json-file>               ex: "home/namespace.json/namespace view"
#     <query-id>                      ex: "/home/namespace.json/namespace view/namespace: test/24/namespace: test/24/a/0"
#         <expr>                      ex: "Row No expression" or "sum(aerospike_namespace_migrate_rx_partitions_remaining{job="aerospike", cluster_name=~"63flash", service=~"172.17.0.7:3000|$^", ns=~"test|$^"})"
#         <results_array>             ex: "[ 0: ]" 
#             [ array-of-results]
#             index: {
#                      metric: ""
#                      value: <array-of-values>
#                      0 : time-in-utc
#                      1 : value  
#                    }

def query_prom_using_get( p_query):
    # print(" running prom-url : ", prometheus_url_to_get)
    http_response = requests.get(prometheus_url_to_get, params={'query': p_query}, verify=False)    
    if "data" in http_response.json():
        data = http_response.json()["data"]
        return data

    # data = http_response.json()["data"]
    # return data

    print("unable to find [data] element in response for query: ", p_query,"\n")
    return ""

    # result = data["result"]    
    # print( data)
    # print(" \t\t ", result)
    
def run_query_and_fetch_result_json(p_query):    
    # print(p_query)
    l_data = query_prom_using_get(p_query )
    
    if len(l_data)>0:    
        # TODO: we need to check success/failure 
        return l_data["result"] 
    return ""
    
def is_dashboard_in_ignorelist(p_key):
    
    # return False
    return p_key in g_ignore_list_dashboards
    
def is_key_query_in_ignorelist(p_query):
    return (p_query.lower() in g_ignore_list_queries)

def fetch_dashboard_name(p_key):
    parts = p_key.split("/")
    for ele in parts:
        if ele.endswith(".json"):
            return ele

    return ""

def make_dashboard_key(p_entry):
    l_key = p_entry["folder"] + "/" + p_entry["dashboard_file"]+"/" + p_entry["dashboard_name"] 
    return l_key.lower()

def make_expression_key(p_entry): 
    l_key = ""
    for p_entry_key in p_entry:
        if "expr" not in p_entry_key:
            l_key = l_key + "/" + p_entry[ p_entry_key]
        
    return l_key.lower()

def read_queries_from_file(p_filename):
    fd_queries = open( p_filename, "r")   
    map_key_and_query = {}
    
    while True:
        line = fd_queries.readline()
 
        if not line:
            break
        # from key=value pair, split
        db_data = json.loads( line)
        
        # key, value pair
        db_entry = db_data["entry"]
        db_key = make_dashboard_key( db_entry)   
        db_entries= []  
        if db_key in map_key_and_query:
            db_entries = map_key_and_query[db_key]
        # else:
        #     print(" adding key ", db_key)
        #     map_key_and_query[db_key] = [db_entry]
        db_entries.append( db_entry)
        map_key_and_query[db_key] = db_entries
        
        # if is_dashboard_in_ignorelist( key):
        #     if is_key_query_in_ignorelist( key) or is_key_query_in_ignorelist( cleaned_str):
        #         print( cleaned_str)

    # print( len(map_key_and_query[ list(map_key_and_query.keys())[0]] ))
    return map_key_and_query

def process_queries_of_db(p_map_of_entries, p_dashboardname):
    l_db_all_query_results= {}
    for key in p_map_of_entries:
        is_dboard_ignored = is_dashboard_in_ignorelist( p_dashboardname) 
        
        # only if dashboard is not in-ignore list
        if p_dashboardname.lower() in key :
            if is_dboard_ignored:
                print("\tNOT Executing, ", p_dashboardname," as it is in ignore-list \t key: ", key)    
            else:
                entries = p_map_of_entries [ key]
                l_map_query_to_values = run_db_queries( entries)
                l_db_all_query_results[ key]= l_map_query_to_values
    
    return l_db_all_query_results

def run_db_queries(p_entries):
    map_query_to_values = {}
    for i_entry in p_entries:
        l_expr = i_entry["expr"]
        l_query_key = make_expression_key( i_entry)
        
        # if query is ignore-list, then execute
        #
        # print( l_query_key, "\t", l_expr)
        # checking if ignore list here so we can 
        if is_key_query_in_ignorelist(l_expr) or len(l_expr)==0:
            # no_result_dct = {"metric":{"name":"ignored-expression"}, "value":["0":"Ignored query as it is in ignore-query-list"]}
            map_expr_and_result = {"expr": l_expr, "results_array": "Ignored query as it is in ignore-query-list or empty"}      
            map_query_to_values[ l_query_key ] = map_expr_and_result
        else:    
            l_query_results = run_query_and_fetch_result_json( l_expr)  
            
            map_expr_and_result = {"expr": l_expr, "results_array": l_query_results}      
            map_query_to_values[ l_query_key ] = map_expr_and_result
        
            # print( l_expr)
        
    return map_query_to_values

def save_query_results_to_file(p_filename, p_dict_db_query_results):
    with open( p_filename, "w") as outfile:
        json.dump( p_dict_db_query_results, outfile)
    
def run_queries( p_filename):
    # a map of K:V "folder/dashboard_filename/dashboard_name": [ <list-of-complete-entries>]
    map_key_and_entries = read_queries_from_file( p_filename)

    l_all_db_query_results = {}

    for e in g_dashboard_names:
        print("run_queries for dashboard: ", e)
        l_query_results = process_queries_of_db(map_key_and_entries, e )
        l_all_db_query_results.update( l_query_results)
        # print("Completed processing p_dashboardname: ", e, "\t len-of-elements: ", len(l_query_results))
    
    # if p_savetofile:
    #     outfile = open( fn_mockquery_results, "w")
    #     json.dump( l_all_db_query_results, outfile)
    #     outfile.close()
    return l_all_db_query_results
  
# main execution
if __name__ == "__main__":
    # use this to generate data for baseline
    from globals import prometheus_url
    from globals import fn_fullform_queries, fn_baseline_results

    l_all_db_query_results = run_queries( fn_fullform_queries)
    save_query_results_to_file( fn_baseline_results, l_all_db_query_results )
    