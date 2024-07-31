import requests
import json
import os

# Configuration
cpq_base_url = os.getenv('PYTHON_INPUT_URL')
client_id = os.getenv('PYTHON_INPUT_Username')
client_secret = os.getenv('PYTHON_INPUT_Password')

# Custom field details
custom_field_name = "Created By"
custom_field_ID = 209

# Authenticate and get access token
def authenticate(client_id, client_secret):
    auth_url = f"{cpq_base_url}basic/api/token"
    auth_payload = {
        "grant_type": "password",
        'username': client_id,
        'password': client_secret,
        'scope': 'configurations_admin'
    }
    response = requests.post(auth_url, data=auth_payload)
    response.raise_for_status() 
    return response.json()['access_token']

# Check if custom field exists
def custom_field_exists(token, field_name):
    headers = {"Authorization": f"Bearer {token}"}
    check_url = f"{cpq_base_url}api/quote/v1/quoteCustomField?$filter=name eq '{field_name}'"
    response = requests.get(check_url, headers=headers)
    print("Checking if custom field exists:", response.json())  
    if response.status_code == 200:
        data = response.json()
        if data and 'pagedRecords' in data and len(data['pagedRecords']) > 0:
            return True
        else:
            return False
    else:
        print(f"Failed to fetch attributes: {response.status_code}, {response.text}")
        return False

# Create custom field
def create_custom_field(token, field_name):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "Name": field_name,
        "Label": "R T M M",
        "Description": "Description of the new quote custom field",
        "type": "FreeForm",
        "IsActive": True,
        "IsMandatory": False,
        "DefaultValue": "Default Value",
        "CalculationType": None
    }
    create_url = f"{cpq_base_url}api/quote/v1/quoteCustomField"
    response = requests.post(create_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

# Update custom field
def update_custom_field(token, field_name):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "id": custom_field_ID,
        "name": field_name,
        "tabRank": 0,
        "showOnPlaceOrder": False,
        "isProtected": False,
        "isSensitive": False,
        "showInTab": [5],
        "implementation": "",
        "triggerSaveAction": True,
        "calculationRank": 0,
        "type": "FreeForm",
        "stdAttributeCode": 0,
        "attributeName": "",
        "label": "Days",
        "translations": [],
        "userTypeLabels": []
    }
    update_url = f"{cpq_base_url}api/quote/v1/quoteCustomField/{custom_field_ID}"
    response = requests.put(update_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

# Main function
def main():
    try:
        token = authenticate(client_id, client_secret)
        if custom_field_exists(token, custom_field_name):
            print(f"Custom field '{custom_field_name}' exists. Updating...")
            update_response = update_custom_field(token, custom_field_name)
            print("Update response:", update_response)
        else:
            print(f"Custom field '{custom_field_name}' does not exist. Creating...")
            create_response = create_custom_field(token, custom_field_name)
            print("Create response:", create_response)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
