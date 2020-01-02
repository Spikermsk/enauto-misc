#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to create/update
organizations and their networks in the Cisco DevNet sandbox.
Note that you can use the Enterprise or Small Business sandboxes
with this script (or a production deployment).
"""

import sys
import json
from meraki_helpers import find_id_by_name, req


def main(net_name):
    """
    Execution begins here.
    """

    # First, get all organizations
    orgs = req("organizations").json()

    # See if supplied org_name is already present by looping
    # over all collected organizations
    org_id = find_id_by_name(orgs, "devnet sandbox")

    # If we didn't find the organization
    if not org_id:
        raise ValueError("could not find 'devnet sandbox' organization")

    # Second, get all networks inside that organization
    nets = req(f"organizations/{org_id}/networks").json()

    # See if supplied net_name is already present by looping
    # over all collected organization networks
    net_id = find_id_by_name(nets, net_name)

    # If we didn't find the network
    if not net_id:
        raise ValueError(f"could not find '{net_name}' organization")

    # Load in the webhooks to add from the JSON file
    with open("add_webhooks.json", "r") as handle:
        webhooks = json.load(handle)

    # For each webhook to add
    for webhook in webhooks:

        # Add each webhook server individually
        print(f"adding webhook '{webhook['name']}'")
        if not webhook["url"].lower().startswith("https"):
            print(" url is not 'https', skipping")
            continue
        add_http = req(
            f"networks/{net_id}/httpServers", method="post", json=webhook
        ).json()

        # Send a test webhook to each server based on URL
        print(f"testing webhook '{webhook['name']}'")
        test_http = req(
            f"networks/{net_id}/httpServers/webhookTests",
            method="post",
            json={"url": webhook["url"]},
        ).json()

        # Ensure the webhooks are enqueued; check the individual
        # webservers manually to ensure success
        if test_http["status"] != "enqueued":
            raise ValueError("webhook test failed: {test_http['status']}")

    # Collect the current webhooks and print them as confirmation
    net_http = req(f"networks/{net_id}/httpServers").json()
    print(f"Current webhook receivers for {net_name}:")
    print(json.dumps(net_http, indent=2))


if __name__ == "__main__":
    # Ensure there are exactly 2 CLI arguments (file name, net name)
    if len(sys.argv) != 2:
        print("usage: python build_network.py <net_name>")
        sys.exit(1)

    # Pass in the net name into main()
    main(sys.argv[1])
