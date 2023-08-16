# Test cases
This folder contains test-cases for the dashboards covering dashboard properties, queries and results

## Software and packages required
these test-cases are python3 based and required json and deepdiff packages to execute

## Test groups
<explain categories and list of each-case which are added>
- Dashboard
    - <mention test-case name and a brief one-liner>
- Rows and Panel
- Queries
- Query execution against prometheus db

## Test groupsdata
we have a dump of the metrics data which is used as a mock, we tried to simulate different config and combinations 
these metrics will be imported into a local running prometheus tsdb using promtool

### Step 1
- generate a latest copy of the mock data, 
  - cd tests/processing
  - python3 gen_openmetrics.py
- new mock data is generated into a file called "output.openmetrics.data" with current timestamp with each metric
  
### Step 2
- goto the prometheus storage location where prometheus software is running
  - example /etc/prometheus/data
- copy the file "output.openmetrics.data" to prometheus storage location
- execute command promtool
  - promtool tsdb create-blocks-from output.openmetrics.data /etc/prometheus/data
    - this will create a folder with an alphanumeric name like "01H7ZNBK9HV1GYTW7Y8RFXCM88"

### Steps to execute the tes-cases
TODO: mention the steps
