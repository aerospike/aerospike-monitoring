import json
import requests

api_key = ''   # Update your Datadog API Key.
app_key = ''   # Update your Datadog Application Key.
datadog_site = 'datadoghq.com'  # This is the Datadog site, which can be changed as needed.




# Load the alert rules from the JSON file
with open('aerospike_rules.json') as f:
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
