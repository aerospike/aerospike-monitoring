import json
import argparse
import os

def parse_dashboard_json(json_data, output_file, subfolder_name, json_file_name):
    data = json.loads(json_data)

    dashboard_name = data['title']
    panels = data['panels']

    base_row_title = "base"
    base_row_id = 0
    index_counter = 0  # Reset index_counter for each panel

    row_title = base_row_title
    row_id = base_row_id

    with open(output_file, 'a') as out_file:
        for panel in panels:
            if 'type' not in panel:
                continue

            if panel['type'] == 'row':
                row_title = panel.get('title', base_row_title)
                row_id = panel.get('id', base_row_id)
                index_counter = 0  # Reset index_counter for each panel
            elif panel['type'] == 'grafana-polystat-panel':
                # For 'grafana-polystat-panel', do not change the row_title and row_id
                pass

            if 'title' in panel:
                panel_title = panel['title']
            else:
                panel_title = "No Title"

            if 'id' in panel:
                panel_id = panel['id']
            else:
                panel_id = "No ID"
            index_counter = 0
            if 'targets' in panel:
                targets = panel['targets']
                for target in targets:
                    if 'expr' in target:
                        expr = target['expr']
                    else:
                        if panel['type'] == 'row':
                            expr = "Row No expression"
                        else:
                            expr = "Panel No Expression"
                    if 'refId' in target:
                        refid = target['refId']
                    else:
                        refid = "No RefID"
                    entry = {
                        "folder": subfolder_name,
                        "dashboard_file": json_file_name,
                        "dashboard_name": dashboard_name,
                        "row_title": row_title,
                        "row_id": str(row_id),
                        "panel_name": panel_title,
                        "panel_id": str(panel_id),
                        "refid": refid,
                        "index": str(index_counter),
                        "expr": expr
                    }

                    # Create the entry dictionary
                    entry_dict = {
                        "key": f"{subfolder_name}/{json_file_name}/{dashboard_name}/{row_title}/{row_id}/{panel_title}/{panel_id}/{refid}/{index_counter}",
                        "entry": entry
                    }
                    out_file.write(json.dumps(entry_dict) + "\n")
                    # result = f"{subfolder_name}/{json_file_name}/{dashboard_name}/{row_title}/{row_id}/{panel_title}/{panel_id}/{refid}/{index_counter} = {expr}".replace('\n', ' ')
                    # # print(result)
                    # out_file.write(result + "\n")
                    index_counter += 1

def parse_files(p_args):
    out_file = open(fn_mock_queries, 'w')

    for subfolder_name, _, filenames in os.walk(p_args.folder_path):
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

