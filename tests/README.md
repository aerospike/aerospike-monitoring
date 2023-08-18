# Test cases
This folder contains test-cases for the dashboards covering dashboard properties, queries and results

## Software and packages required
these test-cases are python3 based and required json and deepdiff packages to execute

## Test groups
- Dashboards - Contains testcases involving dashboards.
    - test_dashboard_count
      - compares the count of "dashboard name" (example: Set Dashboard) in a "dashboard file" (example: set.json) with baseline data
    - test_dashboard_names
     -  compares the "dashboard name" in "dashboard file" has been modified with baseline
- Rows
  - This file contains the testcases involving rows.this is next in line after dashboards.
    - test_row_count
      - we check the count of number of row_title and row_id to check if the count has modified in latest dashboard
    - test_row_names
      - we check if row_id or row_title has been modified in mock compared to the old and list the list the changes
- Panels
  - This file contains the testcases involving rows.this is next in line after row.
    - test_panel_count()
      - we check the count of number of panel_name and panel_id to check if the count has changed between baseline and mock
    - test_panel_names()
      - we check if panel_name or panel_id has been modified in mock compared to the old and list the list the changes
- Queries
  - This file contains the testcases involving rows.this is last in hierechy.unlike the previous ones this has four test-cases instead of two.
    - test_refid_and_index_pair_count
      - we check the count of number of refid and index to check if the count has changed between baseline and mock
    - test_refid_and_index_pair_names
      we check the refid and index pairs to determine if order has changed or refid has changed.
    - test_expr_count
      - we check the count of number of expr to check if the count has changed between baseline and mock
    - test_compare_expr_in_dicts
      - we check if any of the expr changed or not
- Query execution against prometheus db

## Mock data for test-cases
we have a dump of the metrics data which is used as a mock, we tried to simulate different config and combinations 
these metrics will be imported into a local running prometheus tsdb using promtool

### Step 1 - How to create mock data
- generate a latest copy of the mock data, 
  - cd tests/processing
  - python3 gen_openmetrics.py
- new mock data is generated into a file called "output.openmetrics.dat" with current timestamp with each metric
  
### Step 2 - How to import the mock data into Prometheus
- goto the prometheus storage location where prometheus software is running
  - example /etc/prometheus/data
- copy the file "output.openmetrics.dat" to prometheus storage location
- execute command promtool
  - promtool tsdb create-blocks-from output.openmetrics.dat /etc/prometheus/data
    - in /etc/prometheus/data folder this will create a sub-folder with an alphanumeric name like "01H7ZNBK9HV1GYTW7Y8RFXCM88"

### Steps to execute the test-cases
  - first save all the required files in correct locations.
  - there are two methods to run the test cases now:-
    - run them using standard method like using any python interpreter
      - example:- python3 test_dashboards.py
    - run them using pytest
