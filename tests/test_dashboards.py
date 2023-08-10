
import requests

filename_baseline_queries = "mockdata/baseline_dashboard.queries"
filename_mock_queries = "mockdata/mock_dashboard.queries"

baseline_dict_queries = {}
mock_dict_queries = {}

def read_dashboard_queris(p_filename):
    dict_queries = {}
    fd_queries = open( p_filename, "r")   
    
    while True:
        line = fd_queries.readline()
 
        if not line:
            break
        
        # split key and values
        parts = line.split(" = ",1)
        dict_queries[ parts[0]] = parts[1]
    
    return dict_queries

# begin test-cases

def read_unique_dashboard_names(p_dict):
    dict_db_names = {}
    # unique dashboard names from baseline
    for key in p_dict:
        parts = key.split("/")
        for ele in parts:
            if ele.endswith(".json"):
               dict_db_names[ ele ] = ele
    
    return dict_db_names

# 
def test_dashboards_count():   
    # unique dashboard names from baseline and mock
    bl_dict_db_names = read_unique_dashboard_names( baseline_dict_queries)
    mk_dict_db_names = read_unique_dashboard_names( mock_dict_queries)
               
    # compare 
    # print( "test_dashboards_count: " + len(bl_dict_db_names) == len(mk_dict_db_names) )
    assert len(bl_dict_db_names) == len(mk_dict_db_names)

def test_dashboards_namematch():   
    # unique dashboard names from baseline and mock
    bl_dict_db_names = read_unique_dashboard_names( baseline_dict_queries)
    mk_dict_db_names = read_unique_dashboard_names( mock_dict_queries)
               
    # compare 
    new_set = ( set(bl_dict_db_names) - set( mk_dict_db_names))
    assert len(new_set)==0

def test_dashboards_namematch_two():   
    # unique dashboard names from baseline and mock
    bl_dict_db_names = read_unique_dashboard_names( baseline_dict_queries)
    mk_dict_db_names = read_unique_dashboard_names( mock_dict_queries)
               
    # compare 
    new_set = ( set(bl_dict_db_names) - set( mk_dict_db_names))
    assert len(new_set)>0
    
    
# end test-cases

    
# main exeuction   
# step-1 read the queries = baseline and mock
baseline_dict_queries = read_dashboard_queris(filename_baseline_queries)
mock_dict_queries = read_dashboard_queris(filename_mock_queries)

# call each test-case
test_dashboards_count()        
test_dashboards_namematch()
test_dashboards_namematch_two()