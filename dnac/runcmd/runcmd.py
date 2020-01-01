#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the command runner tool on
Cisco DNA center via API calls.
"""

import requests
from auth_token import get_token


def main():
    """
    Execution begins here.
    """

    # Reuse the get_token() function from before. If it fails
    # allow exception to crash program
    # https://developer.cisco.com/docs/dna-center-api-1210/
    host = "sandboxdnac2.cisco.com"
    token = get_token(host)

    # Define headers for GET and POST requests using the collected token
    get_headers = {"Accept": "application/json", "X-Auth-Token": token}
    post_headers = {"Content-Type": "application/json", "X-Auth-Token": token}

    # Collect the list of routers using query parameters
    router_params = {"type": ["s1", "s2"]}
    get_resp = requests.get(
        f"https://{host}/dna/intent/api/v1/network-device",
        headers=get_headers,
        params=router_params,
    )
    get_resp.raise_for_status()

    device_uuids = []  # need to write logic and get UUIDs

    # Build the HTTP body for which tells DNAC which commands to run
    # on which devices (identified by UUID)
    command_body = {
        "commands": [
            "show ip interface brief",
            "show inventory",
            "show version",
        ],
        "deviceUuids": device_uuids,
    }

    # Issue POST request using the command_body just built
    post_resp = requests.post(
        f"https://{host}/dna/intent/api/v1/network-device-poller/cli/read-request",
        headers=post_headers,
        json=command_body,
    )
    post_resp.raise_for_status()


if __name__ == "__main__":
    main()
