
import requests

filename_baseline_queries = "mockdata/baseline_dashboard.queries"
filename_mock_queries = "mockdata/mock_dashboard.queries"

baseline_dict_queries = {}
mock_dict_queries = {}

# def read_dashboard_queris(p_filename):
#     dict_queries = {}
#     fd_queries = open( p_filename, "r")   
    
#     while True:
#         line = fd_queries.readline()
 
#         if not line:
#             break
        
#         # split key and values
#         parts = line.split(" = ",1)
#         dict_queries[ parts[0]] = parts[1]
    
#     return dict_queries

# # begin test-cases

# def read_unique_dashboard_names(p_dict):
#     dict_db_names = {}
#     # unique dashboard names from baseline
#     for key in p_dict:
#         parts = key.split("/")
#         for ele in parts:
#             if ele.endswith(".json"):
#                dict_db_names[ ele ] = ele
    
#     return dict_db_names

# # 
# def test_dashboards_count():   
#     # unique dashboard names from baseline and mock
#     bl_dict_db_names = read_unique_dashboard_names( baseline_dict_queries)
#     mk_dict_db_names = read_unique_dashboard_names( mock_dict_queries)
               
#     # compare 
#     # print( "test_dashboards_count: " + len(bl_dict_db_names) == len(mk_dict_db_names) )
#     assert len(bl_dict_db_names) == len(mk_dict_db_names)

# def test_dashboards_namematch():   
#     # unique dashboard names from baseline and mock
#     bl_dict_db_names = read_unique_dashboard_names( baseline_dict_queries)
#     mk_dict_db_names = read_unique_dashboard_names( mock_dict_queries)
               
#     # compare 
#     new_set = ( set(bl_dict_db_names) - set( mk_dict_db_names))
#     assert len(new_set)==0

# def test_dashboards_namematch_two():   
#     # unique dashboard names from baseline and mock
#     bl_dict_db_names = read_unique_dashboard_names( baseline_dict_queries)
#     mk_dict_db_names = read_unique_dashboard_names( mock_dict_queries)
               
#     # compare 
#     new_set = ( set(bl_dict_db_names) - set( mk_dict_db_names))
#     assert len(new_set)==0
    
    
# end test-cases

def read_dashboard_queries(p_filename):
    dict_queries = {}
    fd_queries = open( p_filename, "r")   
    dict_queries = parse_queries_to_dict(fd_queries)
    return dict_queries

def parse_queries_to_dict(queries):
    result = {}
    
    for query in queries:
        parts = query.strip().split(' = ')
        if len(parts) == 2:
            key = parts[0]
            value = parts[1].strip()  # Remove leading/trailing whitespace
            
            # Parsing key
            key_parts = key.split('/')
            if len(key_parts) >= 9:  # Adjusted for the dashboard name
                folder = key_parts[0]
                dashboard_file = key_parts[1]
                dashboard_name = key_parts[2]  # Added dashboard name
                row_title = key_parts[3]
                row_id = key_parts[4]
                panel_name = key_parts[5]  # Adjusted for the dashboard name
                panel_id = key_parts[6]  # Adjusted for the dashboard name
                refid = key_parts[7]  # Adjusted for the dashboard name
                index = key_parts[8]  # Adjusted for the dashboard name
                
                # Constructing dictionary entry
                entry = {
                    "folder": folder,
                    "dashboard_file": dashboard_file,
                    "dashboard_name": dashboard_name,
                    "row_title": row_title,
                    "row_id": row_id,
                    "panel_name": panel_name,
                    "panel_id": panel_id,
                    "refid": refid,
                    "index": index,
                    "expr": value
                }
                
                result[key] = entry
    
    return result

def list_unique_folders(dictionary):
    unique_folders = set()
    for key in dictionary:
        entry = dictionary[key]
        unique_folders.add(entry["folder"])
    return list(unique_folders)

def list_unique_dashboards_within_folder(dictionary, folder_name):
    unique_dashboards = set()
    for key in dictionary:
        entry = dictionary[key]
        if entry["folder"] == folder_name:
            unique_dashboards.add((entry["dashboard_file"], entry["dashboard_name"]))
    return list(unique_dashboards)

def list_rownames_in_dashboard(data_dict, folder, dashboard_name):
    unique_row_info = {}

    row_id_to_name = {}
    
    for key, entry in data_dict.items():
        
        if entry["folder"] == folder and entry["dashboard_name"] == dashboard_name:
            row_id = entry["row_id"]
            row_name = entry["row_title"]

            if row_id in row_id_to_name:
                # print( " row_id: ", row_id)
                if row_id_to_name[row_id] == row_name:
                    unique_row_info[ row_id] = row_name
            else:
                row_id_to_name[row_id] = row_name

    return unique_row_info

def list_panelnames_in_row(dictionary, folder, dashboard_file, row_id):
    unique_panelnames = set()
    for key in dictionary:
        entry = dictionary[key]
        if entry["folder"] == folder and entry["dashboard_file"] == dashboard_file and entry["row_id"] == row_id:
            unique_panelnames.add((entry["panel_name"], entry["panel_id"]))
    return list(unique_panelnames)

def test_folders_matching():
    old_folders = list_unique_folders(baseline_dict_queries)
    new_folders = list_unique_folders(mock_dict_queries)
    assert ((set(old_folders) - set(new_folders)) == set()) and ((set(new_folders) - set(old_folders)) == set())

def test_count_dashboards():
    for folder in common_folders:
        old_dashboards = list_unique_dashboards_within_folder(baseline_dict_queries, folder)
        new_dashboards = list_unique_dashboards_within_folder(mock_dict_queries, folder)
        assert ((set(old_dashboards) - set(new_dashboards)) == set()) and ((set(new_dashboards) - set(old_dashboards)) == set())

def test_dashboards_matching(baseline_dict_queries, mock_dict_queries, folder_name):
    old_dashboards = list_unique_dashboards_within_folder(baseline_dict_queries, folder_name)
    new_dashboards = list_unique_dashboards_within_folder(mock_dict_queries, folder_name)
    
    missing_in_new = set(old_dashboards) - set(new_dashboards)
    new_in_new = set(new_dashboards) - set(old_dashboards)
    
    if missing_in_new or new_in_new:
        print(f"Dashboard differences in folder '{folder_name}':")
        if missing_in_new:
            print("  Dashboards missing in new file:", missing_in_new)
        if new_in_new:
            print("  New dashboards in new file:", new_in_new)
    else:
        print(f"All dashboards in folder '{folder_name}' matched.")

def test_count_row_names(baseline_dict_queries, mock_dict_queries, folder, dashboard_file):
    old_rownames = list_rownames_in_dashboard(baseline_dict_queries, folder, dashboard_file)
    new_rownames = list_rownames_in_dashboard(mock_dict_queries, folder, dashboard_file)
    
    if len(old_rownames) != len(new_rownames):
        print(f"Different row name counts for folder '{folder}' and dashboard '{dashboard_file}'")
    else:
        print(f"Row name counts match for folder '{folder}' and dashboard '{dashboard_file}'")

def test_rows_are_matching(baseline_dict_queries, mock_dict_queries, folder, dashboard_file):
    old_rownames = list_rownames_in_dashboard(baseline_dict_queries, folder, dashboard_file)
    new_rownames = list_rownames_in_dashboard(mock_dict_queries, folder, dashboard_file)
    
    missing_in_new = set(old_rownames) - set(new_rownames)
    new_in_new = set(new_rownames) - set(old_rownames)
    
    if missing_in_new or new_in_new:
        print(f"Row differences in folder '{folder}' and dashboard '{dashboard_file}':")
        if missing_in_new:
            print("  Rows missing in new file:", missing_in_new)
        if new_in_new:
            print("  New rows in new file:", new_in_new)
    else:
        print(f"All rows in folder '{folder}' and dashboard '{dashboard_file}' matched.")

def test_count_panels(baseline_dict_queries, mock_dict_queries, folder, dashboard_file, row_id):
    old_panelnames = list_panelnames_in_row(baseline_dict_queries, folder, dashboard_file, row_id)
    new_panelnames = list_panelnames_in_row(mock_dict_queries, folder, dashboard_file, row_id)
    
    if len(old_panelnames) != len(new_panelnames):
        print(f"Different panel name counts for folder '{folder}', dashboard '{dashboard_file}', and row '{row_id}'")
    else:
        print(f"Panel name counts match for folder '{folder}', dashboard '{dashboard_file}', and row '{row_id}'")

# 
def test_panels_are_matching(baseline_dict_queries, mock_dict_queries, folder, dashboard_file, row_id):
    old_panelnames = list_panelnames_in_row(baseline_dict_queries, folder, dashboard_file, row_id)
    new_panelnames = list_panelnames_in_row(mock_dict_queries, folder, dashboard_file, row_id)
    
    missing_in_new = set(old_panelnames) - set(new_panelnames)
    new_in_new = set(new_panelnames) - set(old_panelnames)
    
    if missing_in_new or new_in_new:
        print(f"Panel differences in folder '{folder}', dashboard '{dashboard_file}', and row '{row_id}':")
        if missing_in_new:
            print("  Panels missing in new file:", missing_in_new)
        if new_in_new:
            print("  New panels in new file:", new_in_new)
    else:
        print(f"All panels in folder '{folder}', dashboard '{dashboard_file}', and row '{row_id}' matched.")

print(list_rownames_in_dashboard(baseline_dict_queries,"home","cluster.json"))

baseline_dict_queries = read_dashboard_queries(filename_baseline_queries)
mock_dict_queries = read_dashboard_queries(filename_mock_queries)

baseline_unique_folders = list_unique_folders(baseline_dict_queries)
unique_folders_new = list_unique_folders(mock_dict_queries)

# Test if the folders match
common_folders = set(list_unique_folders(baseline_dict_queries))&set(list_unique_folders(mock_dict_queries))

# test_folders_matching()
# test_count_dashboards()

# TODO: kept for reference, will be removed
# # For each folder in baseline_dict_queries, perform the following steps
# for folder in common_folders:
#     # Get unique dashboards within the folder from both dictionaries
#     unique_dashboards_old = list_unique_dashboards_within_folder(baseline_dict_queries, folder)
#     unique_dashboards_new = list_unique_dashboards_within_folder(mock_dict_queries, folder)
#     common_dashboards = set(unique_dashboards_old)&set(unique_dashboards_new)

#     # Test if the dashboard counts match
#     test_count_dashboards()
    
#     # For each dashboard in the folder, perform the following steps
#     for dashboard in common_dashboards:
#         # Get unique row names within the dashboard
#         unique_row_names_old = list_rownames_in_dashboard(baseline_dict_queries, folder, dashboard)
#         unique_row_names_new = list_rownames_in_dashboard(mock_dict_queries, folder, dashboard)
        
#         # Test if the row name counts match
#         test_count_row_names(baseline_dict_queries, mock_dict_queries, folder, dashboard)
        
#         # Test if the row names within the dashboard match
#         test_rows_are_matching(baseline_dict_queries, mock_dict_queries, folder, dashboard)
        
#         # For each row in the dashboard, perform the following steps
#         print(unique_row_names_old)
#         for row_title, row_id in unique_row_names_old:
#             # Get unique panel names within the row
#             unique_panel_names_old = list_panelnames_in_row(baseline_dict_queries, folder, dashboard, row_id)
#             unique_panel_names_new = list_panelnames_in_row(mock_dict_queries, folder, dashboard, row_id)
            
#             # Test if the panel name counts match
#             test_count_panels(baseline_dict_queries, mock_dict_queries, folder, dashboard, row_id)
            
#             # Test if the panel names within the row match
#             test_panels_are_matching(baseline_dict_queries, mock_dict_queries, folder, dashboard, row_id)


list_rownames_in_dashboard(baseline_dict_queries, "home", "Set Dashboard")