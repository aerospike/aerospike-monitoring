import json
import requests

# Prompt user for API key, Application key, and Datadog site
api_key = input("Enter your Datadog API Key: ").strip()
app_key = input("Enter your Datadog Application Key: ").strip()
datadog_site = input("Enter your Datadog site (e.g., datadoghq.com): ").strip()

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
