#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the template programmer tool on
Cisco DNA center via API calls.
"""

import time
import requests
from auth_token import get_token


def main():
    """
    Execution begins here.
    """

    # The DNA Center reserved sandbox uses a self-signed cert at present,
    # so let's ignore any obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # Reuse the get_token() function from before. If it fails
    # allow exception to crash program
    # https://developer.cisco.com/docs/dna-center-api-1210/
    host = "10.10.20.85"
    token = get_token(host)

    # Define headers for GET and POST requests using the collected token
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": token,
    }
    proj_body = {
        "name": "nickrus_proj",
        "description": "testing some python scripts",
    }
    proj_resp = requests.post(
        f"https://{host}/dna/intent/api/v1/template-programmer/project",
        headers=headers,
        json=proj_body,
        verify=False,
    )
    # Debugging statement to explore the proj_resp body structure
    import json; print(json.dumps(proj_resp.json(), indent=2))
    proj_resp.raise_for_status()

    time.sleep(2)
    task = proj_resp.json()["response"]["taskId"]
    task_resp = requests.get(
        f"https://{host}/dna/intent/api/v1/task/{task}",
        headers=headers,
        verify=False,
    )
    # Debugging statement to explore the task_resp body structure
    import json; print(json.dumps(task_resp.json(), indent=2))
    task_resp.raise_for_status()

    # Extract the task data, which indicates if an error occurred
    # Debugging statement to explore the task_resp body structure
    # print(json.dumps(task_resp.json(), indent=2))
    task_data = task_resp.json()["response"]

    # Test for isError being true; if so, raise error with progress message
    if task_data["isError"]:
        raise ValueError(f"Async task error: {task_data['progress']}")

    proj_id = task_data["data"]
    temp_body = {
        "name": "nickrus_temp",
        "composite": False,
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs",
                "productSeries": "Cisco Catalyst 9300 Series Switches",
                "productType": "Cisco Catalyst 9300 Switch",
            }
        ],
        "softwareType": "IOS-XE",
        "templateContent": "hostname $hostname\nip ssh version $ssh_ver",
        "templateParams": [
            {
                "parameterName": "hostname",
                "required": True,
                "order": 1,
            },
            {
                "parameterName": "ssh_ver",
                "required": True,
                "order": 2,
            },
        ],
    }
    temp_resp = requests.post(
        f"https://{host}/dna/intent/api/v1/template-programmer/project/{proj_id}/template",
        headers=headers,
        json=temp_body,
        verify=False,
    )
    # Debugging statement to explore the temp_resp body structure
    import json; print(json.dumps(temp_resp.json(), indent=2))
    temp_resp.raise_for_status()

    time.sleep(2)
    task = temp_resp.json()["response"]["taskId"]
    task_resp = requests.get(
        f"https://{host}/dna/intent/api/v1/task/{task}",
        headers=headers,
        verify=False,
    )
    # Debugging statement to explore the task_resp body structure
    import json; print(json.dumps(task_resp.json(), indent=2))
    task_resp.raise_for_status()


if __name__ == "__main__":
    main()
