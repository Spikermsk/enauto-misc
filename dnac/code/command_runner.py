#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the command runner tool on
Cisco DNA center via API calls.
"""

import json
import time
import os
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
    # host = "dnac.aws.labrats.se"
    # host = "sandboxdnac2.cisco.com"
    host = "10.10.20.85"
    token = get_token(host)

    # Define headers for GET and POST requests using the collected token
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": token,
    }

    # Collect the list of routers using query parameters. Specifically,
    # we only want distribution switches (one of them is currently down)
    search_params = {
        "family": "Switches and Hubs",
        "type": "Cisco Catalyst 9300 Switch",
    }
    get_resp = requests.get(
        f"https://{host}/dna/intent/api/v1/network-device",
        headers=headers,
        params=search_params,
        verify=False,
    )
    get_resp.raise_for_status()

    # Debugging statement to explore the get_resp body structure
    # print(json.dumps(get_resp.json(), indent=2))

    device_uuids = []
    for dev in get_resp.json()["response"]:
        if not dev["errorCode"]:
            print(f"Adding {dev['hostname']}: {dev['instanceUuid']}")
            device_uuids.append(dev["instanceUuid"])
        else:
            print(f"Ignoring {dev['hostname']}: {dev['errorCode']}")

    # Build the HTTP body which tells DNAC which commands to run
    # on which devices (identified by UUID)
    # 'commands' maximum is 5
    # 'device_uuids' maximum is 20
    command_body = {
        "commands": ["show inventory", "show version", "show badstuff"],
        "deviceUuids": device_uuids,
    }

    # Issue POST request using the command_body just built
    post_resp = requests.post(
        f"https://{host}/dna/intent/api/v1/network-device-poller/cli/read-request",
        headers=headers,
        json=command_body,
        verify=False,
    )
    # Debugging statement to explore the post_resp body structure
    # print(json.dumps(post_resp.json(), indent=2))
    post_resp.raise_for_status()

    # Wait for async job to complete
    #time.sleep(10)

    # Query DNA center for the status of the specific task ID
    task = post_resp.json()["response"]["taskId"]
    task_resp = requests.get(
        f"https://{host}/dna/intent/api/v1/task/{task}",
        headers=headers,
        verify=False,
    )
    import pdb; pdb.set_trace()
    task_resp.raise_for_status()

    # Extract the task data, which indicates if an error occurred
    # Debugging statement to explore the task_resp body structure
    # print(json.dumps(task_resp.json(), indent=2))
    task_data = task_resp.json()["response"]

    # Test for isError being true; if so, raise error with progress message
    if task_data["isError"]:
        raise ValueError(f"Async task error: {task_data['progress']}")

    # Parse the file dictionary from the progress string, and download file
    file_dict = json.loads(task_data["progress"])
    file_resp = requests.get(
        f"https://{host}/dna/intent/api/v1/file/{file_dict['fileId']}",
        headers=headers,
        verify=False,
    )
    file_resp.raise_for_status()

    # Debugging statement to explore the file_resp body structure
    # print(json.dumps(file_resp.json(), indent=2))

    # Create outputs directory if it doesn't already exist
    file_dir = "outputs"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Loop through list of dicts in the file response
    for item in file_resp.json():
        uuid = item["deviceUuid"]

        # Loop over each type of result: SUCCESS, FAILURE, BLACKLISTED
        # along with the command dict inside
        for result, cmd_dict in item["commandResponses"].items():

            # Loop over the command dict of command/output pairs
            for cmd, output in cmd_dict.items():
                print(f"{uuid}: {cmd} -> {result}")

                # Use underscores in filenames instead of spaces (cleaner)
                cmd_u = cmd.replace(" ", "_")
                with open(f"{file_dir}/{uuid}_{cmd_u}.txt", "w") as handle:
                    handle.write(output)


if __name__ == "__main__":
    main()
