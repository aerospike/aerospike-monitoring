import requests
import json

from deepdiff import DeepDiff

from processing.run_queries import save_query_results_to_file
from processing.run_queries import run_queries, is_key_query_in_ignorelist
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
    
def compare_json_elements( p_key, p_base_db_elements, p_mock_db_elements):
    l_results = []
    
    # step-1 - loop this array using baseline keys 
    for base_key in p_base_db_elements.keys():
        first_query_objects = p_base_db_elements [ base_key]
        if base_key in p_mock_db_elements:
            second_query_objects = p_mock_db_elements[ base_key]
            first_expr = first_query_objects["expr"]
            second_expr = second_query_objects["expr"]
            if not is_key_query_in_ignorelist(first_expr) and can_process_expression( p_key, base_key, first_expr, second_expr):            
                first_results_arr= first_query_objects["results_array"]
                second_results_arr= second_query_objects["results_array"]            
                if can_process_results(p_key, base_key, first_results_arr, second_results_arr):
                    compare_2_results( p_key, base_key, first_results_arr, second_results_arr)
        else:
            l_results.append("EXPR Mismatch: in dashboard "+ p_key + " at row/panel " + base_key +" - expression is not available in latest results ")                        
                            
    return l_results 

def compare_2_results(p_db_key, p_row_panel_key, p_first_results_arr, p_second_results_arr):
    first_metric_element = p_first_results_arr[0]                
    second_metric_element = p_second_results_arr[0]
    if first_metric_element["metric"] == second_metric_element["metric"]:
        # print( "\n first_metric_element", first_metric_element, " -- \n second_metric_element", second_metric_element )
        first_metric_value = first_metric_element["value"]
        second_metric_value = second_metric_element["value"]
        # if value length is same, then we compare the value ignoring the time-factor
        #    value:[<time-in-UTC>, "metric-value"]   example: [1692256189.538, '0']
        if len(first_metric_value) == len(second_metric_value):
            if first_metric_value[1] == second_metric_value[1]:
                # print("MATCHING Metrics/Values: in dashboard "+p_db_key+ " at row/panel " + p_row_panel_key +" - "+ " both metrics and values are matching !!!" )   
                return True            
        else:
            return False    
        
    return False

def can_process_results(p_db_key, p_row_panel_key, p_first_results_arr, p_second_results_arr):
    if ( len(p_first_results_arr) == len(p_second_results_arr)) :
        # print( "len(p_first_results_arr): ", len(p_first_results_arr),"\t len(p_second_results_arr): ", len(p_second_results_arr) )
        return True
        # if len(p_first_results_arr)>0 :
    
    # print("RESULTS Mismatch in dashboard " + p_db_key+ " at row/panel " + p_row_panel_key + " - results_array sizes are not matching ")        
    return False

def can_process_expression(p_db_key, p_row_panel_key, p_first_expr, p_second_expr):
    if ( p_first_expr.strip().lower() != p_second_expr.strip().lower()):
            # print("EXPR Mismatch: in dashboard "+p_db_key+ " at row/panel " + p_row_panel_key +" - " + p_first_expr + " expression is not matching with "+ p_second_expr)
            return False

    return True

# test-case to check the json object for each dashboard, this works at dashboard-level does not dig into individually into each json-object-childs
#    
def test_dashboard_entry_counts():
    l_all_baseline_results = read_baseline_query_results()
    l_mock_results = read_mock_data_query_results()

    l_results = []
    
    for e in l_all_baseline_results.keys():
        if e in l_mock_results :
            if len( l_all_baseline_results[ e]) != len(l_mock_results[e]) :
                print("MISMATCH: in dashboard  " + e + " - baseline-counts: ", len( l_all_baseline_results[ e]), " mock count: ", len(l_mock_results[e]))    
        else:
            l_results.append("EXPR Mismatch: in dashboard "+ e +" - expression is not available in latest results ")

    assert len( l_results)==0, str(l_results)  

def test_dashboard_json_entries():
    l_all_baseline_results = read_baseline_query_results()
    l_mock_results = read_mock_data_query_results()
    
    l_results = []
    
    for e in l_all_baseline_results.keys():        
        if e in l_mock_results:
            l_base_db_elements = l_all_baseline_results[ e]
            l_mock_db_elements = l_mock_results[ e]
            l_results.append( compare_json_elements( e, l_base_db_elements, l_mock_db_elements ) )
        else:
            l_results.append("EXPR Mismatch: in dashboard "+ e +" - expression is not available in latest results ")
        
    #     result = DeepDiff(l_base_db_elements, l_mock_db_elements)
    #     if len(result)>0:
    #         l_results.append( "Differences observed in "+ e +" - are: "+ str(result))
    
    assert len(l_results)==0, "\nFAILED:\n"+ str(l_results)

def test_dashboard_expr():
    l_all_baseline_results = read_baseline_query_results()
    l_mock_results = read_mock_data_query_results()
    
    l_results = []
    
    for e in l_all_baseline_results.keys():
        l_base_db_elements = l_all_baseline_results[ e]
        if e in l_mock_results:
            l_mock_db_elements = l_mock_results[ e]
            for base_key in l_base_db_elements.keys():
                first_query_objects = l_base_db_elements [ base_key]
                second_query_objects = l_mock_db_elements[ base_key]
                first_expr = first_query_objects["expr"]
                second_expr = second_query_objects["expr"]
                if not is_key_query_in_ignorelist(first_expr) and not can_process_expression(e, base_key, first_expr, second_expr):
                    l_results.append("EXPR Mismatch: in dashboard "+e+ " at row/panel " + base_key +" - " + first_expr + " expression is not matching with "+ second_expr)
        else:
            l_results.append("EXPR Mismatch: in dashboard "+ e +" - expression is not available in latest results ")                        
    
    assert len(l_results)==0, "\nFAILED:\n"+ str( l_results)

def test_dashboard_expr_metrics():
    l_all_baseline_results = read_baseline_query_results()
    l_mock_results = read_mock_data_query_results()
    
    l_results = []
    
    for e in l_all_baseline_results.keys():
        l_base_db_elements = l_all_baseline_results[ e]
        if e in l_mock_results:
            l_mock_db_elements = l_mock_results[ e]
            for base_key in l_base_db_elements.keys():
                first_query_objects = l_base_db_elements [ base_key]
                second_query_objects = l_mock_db_elements[ base_key]
                first_expr = first_query_objects["expr"]
                second_expr = second_query_objects["expr"]
                if not is_key_query_in_ignorelist(first_expr) and can_process_expression(e, base_key, first_expr, second_expr):
                    first_results_arr= first_query_objects["results_array"]
                    second_results_arr= second_query_objects["results_array"]                            
                    if not can_process_results( e, base_key, first_results_arr, second_results_arr):
                        print(first_expr, "\n\t", second_expr, "\n" )
                        l_results.append("FAILED: MISMATCH Metrics/Values: in dashboard "+e+ " at row/panel " + base_key +" - "+ first_expr+" metrics/values are not matching with " + second_expr ) 
    
    assert len(l_results)==0, "\nFAILED:\n"+ str( json.dumps(l_results))
                                        
# main test-cases
if __name__ == "__main__":
    # test_dashboard_expr()
    # test_dashboard_entry_counts()
    test_dashboard_expr_metrics()
    # test_dashboard_expr()
    # test_dashboard_json_entries()    