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
    
    SET_FROM_BASELINE = loop_for_count(baseline_dict_queries, l_keys_arr)    
    SET_FROM_MOCK = loop_for_count(mock_dict_queries, l_keys_arr) 
    
    assert len(SET_FROM_BASELINE) == len(SET_FROM_MOCK),f"{len(SET_FROM_BASELINE)} is baseline and {len(SET_FROM_MOCK)} is mock "
    
#Construct two dicts with coreesponding keys and values.then compare them to to list all errors into two dicts called missing and additional
#and then assert that both missing and additional are empty 
def test_refid_and_index_pair_names():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    SET_FROM_BASELINE = loop_for_names(baseline_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid"],"index")
    SET_FROM_MOCK = loop_for_names(mock_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid"],"index")

    SET_MISSING = loop_for_comparision(SET_FROM_BASELINE,SET_FROM_MOCK)
    SET_ADDITIONAL = loop_for_comparision(SET_FROM_MOCK,SET_FROM_BASELINE)

    assert (len(SET_ADDITIONAL) == 0) and (len(SET_MISSING) == 0),f"{SET_MISSING} are the missing and {SET_ADDITIONAL} are the one added additinally"

#makes two sets and then compares them to get the count
def test_expr_count():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    SET_FROM_BASELINE = loop_for_count(baseline_dict_queries, ["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index","expr"])
    SET_FROM_MOCK = loop_for_count(mock_dict_queries, ["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index","expr"]) 
    assert len(SET_FROM_BASELINE) == len(SET_FROM_MOCK),f"{len(SET_FROM_BASELINE)} is baseline and {len(SET_FROM_MOCK)} is mock "

#Construct two dicts with coreesponding keys and values.then compare them to to list all errors into two dicts called missing and additional
#and then assert that both missing and additional are empty 
def test_compare_exprs_in_dicts():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)
    
    SET_FROM_BASELINE = loop_for_names(baseline_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index"],"expr")
    SET_FROM_MOCK = loop_for_names(mock_dict_queries,["folder","dashboard_file","dashboard_name","row_id","row_title","panel_id","panel_name","refid","index"],"expr")

    SET_MISSING = loop_for_comparision(SET_FROM_BASELINE,SET_FROM_MOCK)
    SET_ADDITIONAL = loop_for_comparision(SET_FROM_MOCK,SET_FROM_BASELINE)

    assert (len(SET_ADDITIONAL) == 0) and (len(SET_MISSING) == 0),f"{SET_MISSING} are the missing and {SET_ADDITIONAL} are the one added additinally"
