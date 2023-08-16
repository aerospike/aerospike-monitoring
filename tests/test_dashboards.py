
import requests
import json

from processing.commons import read_dashboard_queries, loop_for_comparision, loop_for_count, loop_for_names
from configs import fn_baseline_queries, fn_mock_queries

#makes two sets and then compares them to get the count
def test_dashboards_count():

    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)

    SET_FROM_BASELINE = loop_for_count(baseline_dict_queries, ["folder","dashboard_file","dashboard_name"])
    SET_FROM_MOCK = loop_for_count(mock_dict_queries, ["folder","dashboard_file","dashboard_name"]) 
    assert len(SET_FROM_BASELINE) == len(SET_FROM_MOCK),f"{len(SET_FROM_BASELINE)} is baseline and {len(SET_FROM_MOCK)} is mock "

#Construct two dicts with coreesponding keys and values.then compare them to to list all errors into two dicts called missing and additional
#and then assert that both missing and additional are empty 
def test_dashboards_names():
    
    baseline_dict_queries = read_dashboard_queries(fn_baseline_queries)
    mock_dict_queries = read_dashboard_queries(fn_mock_queries)

    SET_FROM_BASELINE = loop_for_names(baseline_dict_queries,["folder","dashboard_file"],"dashboard_name")
    SET_FROM_MOCK = loop_for_names(mock_dict_queries,["folder","dashboard_file"],"dashboard_name")

    SET_MISSING = loop_for_comparision(SET_FROM_BASELINE,SET_FROM_MOCK)
    SET_ADDITIONAL = loop_for_comparision(SET_FROM_MOCK,SET_FROM_BASELINE)
    print(" testing ...")
    
    print(SET_FROM_MOCK )

    assert (len(SET_ADDITIONAL) == 0) and (len(SET_MISSING) == 0),f"{SET_MISSING} are the missing and {SET_ADDITIONAL} are the one added additinally"


# extract queries in to a global variable

if __name__ == "__main__":
    test_dashboards_count()
    test_dashboards_names()