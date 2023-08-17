import requests
import json

from processing.commons import read_dashboard_queries, loop_for_comparision, loop_for_count, loop_for_names, construct_key
from configs import fn_baseline_queries, fn_mock_queries

#makes two sets and then compares them to get the count
def test_refid_and_index_pair_count():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    l_keys_arr = ["folder","dashboard_file","dashboard_name","row_id",
                  "row_title","panel_id","panel_name","refid",
                  "index"]
    
    baseline_set = loop_for_count(baseline_dict_queries, l_keys_arr)    
    mock_set = loop_for_count(mock_dict_queries, l_keys_arr) 
    
    assert len(baseline_set) == len(mock_set),f"{len(baseline_set)} is baseline and {len(mock_set)} is mock "
    
#Construct two dicts with coreesponding keys and values.then compare them to to list all errors into two dicts called missing and additional
#and then assert that both missing and additional are empty 
def test_refid_and_index_pair_names():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    baseline_dict = loop_for_names(baseline_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid"],"index")
    mock_dict = loop_for_names(mock_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid"],"index")

    missing_dict = loop_for_comparision(baseline_dict,mock_dict)
    additional_dict = loop_for_comparision(mock_dict,baseline_dict)

    assert (len(additional_dict) == 0) and (len(missing_dict) == 0),f"{missing_dict} are the missing and {additional_dict} are the one added additinally"

#makes two sets and then compares them to get the count
def test_expr_count():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    baseline_set = loop_for_count(baseline_dict_queries, ["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index","expr"])
    mock_set = loop_for_count(mock_dict_queries, ["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index","expr"]) 
    assert len(baseline_set) == len(mock_set),f"{len(baseline_set)} is baseline and {len(mock_set)} is mock "

#Construct two dicts with coreesponding keys and values.then compare them to to list all errors into two dicts called missing and additional
#and then assert that both missing and additional are empty 
def test_compare_expr_in_dicts():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    baseline_dict = loop_for_names(baseline_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index"],"expr")
    mock_dict = loop_for_names(mock_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index"],"expr")

    missing_dict = loop_for_comparision(baseline_dict,mock_dict)
    additional_dict = loop_for_comparision(mock_dict,baseline_dict)

    assert (len(additional_dict) == 0) and (len(missing_dict) == 0),f"{missing_dict} are the missing and {additional_dict} are the one added additinally"

if __name__ == "__main__":
    test_refid_and_index_pair_count()
    test_refid_and_index_pair_names()
    test_expr_count()
    test_compare_expr_in_dicts