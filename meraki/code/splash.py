#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to create/update
external captive portal (excap) settings on Meraki SSIDs.
"""

import sys
from meraki_helpers import get_network_id, req


def main(org_name, net_name, splash_host):
    """
    Execution begins here.
    """

    # Find the network ID for our reserved instance (or personal org)
    net_id = get_network_id(net_name, org_name)

    # Use the first SSID for configuration, which has some default config
    ssid_number = 0

    # Assemble the SSID base URL and the HTTP PUT request payload
    ssid_base = f"networks/{net_id}/ssids/{ssid_number}"
    ssid_body = {
        "splashPage": "Click-through splash page",
        "authMode": "open",
        "adminSplashUrl": f"http://{splash_host}/index.html",
        "walledGardenEnabled": True,
        "walledGardenRanges": splash_host,
    }

    # Issue the PUT request to update the SSID general parameters
    print(f"Updating SSID {ssid_number} with excap host {splash_host}")
    update_ssid = req(ssid_base, method="put", json=ssid_body).json()

    # Debugging statement to check the updated SSID information
    # import json; print(json.dumps(update_ssid, indent=2))

    # Assemble the splash HTTP PUT request payload
    splash_body = {
        "splashMethod": "Click-through splash page",
        "splashUrl": f"http://{splash_host}/index.html",
        "useSplashUrl": True,
    }

    # Issue the PUT request to update the splash page parameters
    print(f"Update SSID {ssid_number} splash settings")
    update_splash = req(
        f"{ssid_base}/splashSettings", method="put", json=splash_body
    ).json()

    # Debugging statement to check the updated splash information
    # import json; print(json.dumps(update_splash, indent=2))


if __name__ == "__main__":
    # Ensure there are exactly 3 CLI args (file name, net name, splash host)
    if len(sys.argv) != 4:
        print("usage: python splash.py <org_name> <net_name> <splash_host>")
        sys.exit(1)

    # Pass in the arguments into main()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    # python splash.py "Loop Free Consulting" "Home Wireless" splash.njrusmc.net
