import json
import argparse
import os

def parse_dashboard_json(json_data, output_filename, subfolder_name, json_file_name):
    data = json.loads(json_data)

    dashboard_name = data['title']
    panels = data['panels']

    base_row_title = "base"
    base_row_id = 0
    index_counter = 0  # Reset index_counter for each panel

    row_title = base_row_title
    row_id = base_row_id
    
    with open(output_filename, 'a') as out_file:
        # both rows and panels are treated as panels in grafana, with type as "row" for rows
        # print( len(panels))
        for panel in panels:
            # print ("processing panel : ", panel['type'])
            if 'type' not in panel:
                continue
            # if json_file_name=="connectorsview.json":
            if panel['type'] == 'row':
                row_title = panel.get('title', base_row_title)
                row_id = panel.get('id', base_row_id)
                index_counter = 0  # Reset index_counter for each panel
                    
                # this is a row, handle child panels 
            if "panels" in panel:
                print(" len(panel[panels]) ", len(panel["panels"]))
                for p_sub_panel in panel["panels"]:
                    handle_panel(out_file, subfolder_name, json_file_name, dashboard_name, row_title, row_id, p_sub_panel)                            
            else: # this is individual panel without a row
                print("this is a single panel processing")
                handle_panel(out_file, subfolder_name, json_file_name, dashboard_name, row_title, row_id, panel)
                    
                # elif panel['type'] == 'grafana-polystat-panel':
                #     # For 'grafana-polystat-panel', do not change the row_title and row_id
                #     pass
                    
                
def handle_panel(p_out_file, p_subfolder_name, p_json_file_name, p_dashboard_name, p_row_title, p_row_id, p_panel):
    if 'title' in p_panel:
        panel_title = p_panel['title']
    else:
        panel_title = "No Title"
    # print( " panel title ", panel_title)
    # print("processing ... p_row_title: ", p_row_title, "\tpanel_title: ",panel_title)

    if 'id' in p_panel:
        panel_id = p_panel['id']
    else:
        panel_id = "No ID"
            
    index_counter = 0
    # if p_json_file_name=="all_flash.json" or p_json_file_name=="connectorsview.json":
    #     print("panel_title: ", panel_title)
    #     print("processing ... json_file_name: ",p_json_file_name," --- ('targets' in panel)? ", ('targets' in p_panel))
    #     print("'type' in panel ", 'type' in p_panel, "\t panel title:? ", 'title' in p_panel,"\t panel['type'] == 'row': ", p_panel['type'] == 'row')
            
    if ('targets' not in p_panel):
        print(" no targets in the panel... hence ignoring")
    else:
        print(" panel_title: ", panel_title, " \t len(p_panel['targets']): ", len(p_panel['targets']))
        for target in p_panel['targets']:

            refid = "No RefID"
            expr = "Panel No Expression"
            
            if 'expr' in target:
                expr = target['expr']
            else:
                if p_panel['type'] == 'row':
                    expr = "Row No expression"

            if 'refId' in target:
                refid = target['refId']
                    
            entry = {
                "folder": p_subfolder_name,
                "dashboard_file": p_json_file_name,
                "dashboard_name": p_dashboard_name,
                "row_title": p_row_title,
                 "row_id": str(p_row_id),
                "panel_name": panel_title,
                "panel_id": str(panel_id),
                "refid": refid,
                "index": str(index_counter),
                "expr": expr
            }

            # Create the entry dictionary
            entry_dict = {
                "key": f"{p_subfolder_name}/{p_json_file_name}/{p_dashboard_name}/{p_row_title}/{p_row_id}/{panel_title}/{panel_id}/{refid}/{index_counter}",
                "entry": entry
            }
            index_counter += 1
            p_out_file.write(json.dumps(entry_dict) + "\n")

def parse_files(p_args):
    out_file = open(fn_mock_queries, 'w')
    
    print("starting processing of given folder : ", p_args.folder_path)

    for subfolder_name, dirs, filenames in os.walk(p_args.folder_path):
        for filename in filenames:
            if filename.endswith('.json'):
                print(" processing .... "+filename)
                json_file_path = os.path.join(subfolder_name, filename)
                if subfolder_name == p_args.folder_path:
                    current_subfolder_name = "home"
                else:
                    current_subfolder_name = subfolder_name[len( p_args.folder_path) + 1:]  # Get the subfolder name relative to folder_path
                parse_dashboard_json(open(json_file_path).read(), fn_mock_queries, current_subfolder_name, filename)
                
if __name__ == "__main__":
    from globals import fn_mock_queries

    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", help="Path to the folder containing Grafana JSON files")
    args = parser.parse_args()
    parse_files( args)

