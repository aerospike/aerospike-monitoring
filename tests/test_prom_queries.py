import requests
import json

from processing.run_queries import save_query_results_to_file
from processing.run_queries import run_queries
import processing.globals

fn_fullform_queries = "mockdata/queries_to_test.queries"
fn_mockquery_results = "mockdata/mock_query_results.queries"
fn_baseline_results = "mockdata/baseline_query_results.queries"


def read_mock_data_query_results():
    # read
    l_all_db_query_results = run_queries(fn_fullform_queries)
    # save mockdata for reference
    save_query_results_to_file(fn_mockquery_results, l_all_db_query_results)
    
    return l_all_db_query_results

def read_baseline_query_results():
    fd_input_file= open( fn_baseline_results, "r")
    l_all_db_query_results = json.load( fd_input_file)
    fd_input_file.close()
    
    return l_all_db_query_results
    
def test_dashboard_entry_counts():
    l_all_baseline_results = read_baseline_query_results()
    l_mock_results = read_mock_data_query_results()
    
    for e in l_all_baseline_results.keys():
        # print(e)
        print(" \t baseline-counts: ", len( l_all_baseline_results[ e]), " \t mock count: ", len(l_mock_results[e]))    

def compare_json_elements():
    l_results = []
    
    return l_results 

def test_dashboard_entry_counts():
    l_all_baseline_results = read_baseline_query_results()
    l_mock_results = read_mock_data_query_results()
    
    for e in l_all_baseline_results.keys():
        l_base_db_elements = l_all_baseline_results[ e]
        l_mock_db_elements = l_mock_results[ e]
        # l_results = compare_json_elements( l_base_db_elements, l_mock_db_elements )
        # print( sorted(l_base_db_elements) == l_base_db_elements.sort() )
    
# main test-cases
test_dashboard_entry_counts()    