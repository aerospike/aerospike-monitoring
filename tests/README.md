# Test cases
This folder contains test-cases for the dashboards covering dashboard properties, queries and results

## Software and packages required
these test-cases are python3 based and required json and deepdiff packages to execute

## Test cases grouping
### validating dashboard, panel, rows and expression 
- Dashboards - contains testcases involving dashboards.
    - test_dashboard_count
      - matches the number of "dashboards" (example: Set Dashboard) in a "dashboard file" (example: set.json) with baseline, reports if there are any dashboard delete / additions
    - test_dashboard_names
     -  matches each "dashboard name" in "dashboard file" has been modified with baseline
- Rows - contains testcases involving rows within a dashboard
    - test_row_count
      - matches the number of rows within a dashboard are same as baseline, reports if there is any delete / additions
    - test_row_names
      - matches each "row title" in each dashboard with baseline, reports if there are any changes
- Panels - contains the testcases involving panels in a rows within a dashboard
  - This file contains the testcases involving rows.this is next in line after row.
    - test_panel_count
      - matches the number of panels in a row within a dashboard, reports if any difference
    - test_panel_names
      - matches each "panel title" in a row within each dashboard with baseline, reports if there are any changes
- Queries - contains the testcases involving queries in a panel 
    - test_refid_and_index_pair_count
      - matches count of queries within a panel in a rows within a dashboard, reports if any changes in the queries
    - test_refid_and_index_pair_names
      - matches each "query" in a panel within each dashboard with baseline, reports if there are any changes

### Steps to execute the test-cases
  - there are two methods to run the test cases now:-
    - run them using standard method like using any python interpreter
      - example:- python3 test_dashboards.py
    - run them using pytest

### query/expression validation
these test-cases are executed against a local prometheus db and the results are compared with a baselined results
this will highlight if any change in queries or adding new labels cause query execution issue or result in null/no results

#### Mock data for test-cases
we have a dump of the metrics data which is used as a mock, we tried to simulate different config and combinations 
these metrics will be imported into a local running prometheus tsdb using promtool

#### Step 1 - How to create mock data

Generate a latest copy of the mock data:

```bash
cd tests/processing
python3 gen_openmetrics.py
```

This creates a file called `output.openmetrics.dat` in `mockdata/` directory with current timestamp for each metric.

#### Step 2 - How to import the mock data into Prometheus

1. Navigate to the Prometheus storage location (e.g., `/etc/prometheus/data`)

2. Copy the `output.openmetrics.dat` file to the Prometheus storage location

3. Run the promtool command to import the data:

```bash
promtool tsdb create-blocks-from openmetrics output.openmetrics.dat /etc/prometheus/data
```

This will create a sub-folder with an alphanumeric name like `01H7ZNBK9HV1GYTW7Y8RFXCM88` in the `/etc/prometheus/data` directory.

