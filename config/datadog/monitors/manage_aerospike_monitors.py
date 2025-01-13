import json
import requests
import sys

def manage_monitors():
    # Prompt user for API key, Application key, and Datadog site
    api_key = sys.argv[1].strip()
    app_key = sys.argv[2].strip()
    datadog_site = sys.argv[3].strip()

    # Load the alert rules from the JSON file
    with open('aerospike_datadog_monitors.json') as f:
        monitors = json.load(f)

    for monitor in monitors:

        url = f'https://{datadog_site}/api/v1/monitor'
        
        # Send the POST request to create the monitor
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'DD-API-KEY': api_key,
                'DD-APPLICATION-KEY': app_key
            },
            json=monitor
        )

        if response.status_code == 200:
            print("Monitor created successfully:", response.json())
        else:
            print("Failed to create monitor. Status code:", response.status_code)
            print("Response:", response.json())
    

if __name__ == '__main__':

    if len( sys.argv)!=4 :
        print("Usage: python3 manage_aerospike_monitors.py <API_KEY> <APP_KEY> <DATADOG_SITE_ID> ")
    else:
        manage_monitors()