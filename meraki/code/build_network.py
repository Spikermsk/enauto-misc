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


def main(org_name, net_name):
    """
    Execution begins here.
    """

    # First, get all organizations
    orgs = req("organizations").json()

    # Print the list of organizations for troubleshooting
    print(json.dumps(orgs, indent=2))

    # See if supplied org_name is already present by looping
    # over all collected organizations
    org_id = find_id_by_name(orgs, org_name)

    # If we didn't find the organization
    if not org_id:
        # Create the organization
        body = {"name": org_name}
        new_org = req("organizations", method="post", json=body).json()
        org_id = new_org["id"]

        # The network cannot possibly exist, so also create the network
        body = {"name": net_name, "type": "appliance"}
        new_net = req(
            f"/organizations/{org_id}/networks", method="post", json=body
        ).json()
        net_id = new_net["id"]

    # Else we did find the organization, don't recreate it
    else:
        print(f"Organization '{org_name}' exists, not recreating")

        # Second, get all networks inside that organization
        nets = req(f"organizations/{org_id}/networks").json()

        # Print the list of organizations for troubleshooting
        print(json.dumps(nets, indent=2))

        # See if supplied net_name is already present by looping
        # over all collected organization networks
        net_id = find_id_by_name(nets, net_name)

        # If we didn't find the network
        if not net_id:
            body = {"name": net_name, "type": "appliance"}
            new_net = req(
                f"/organizations/{org_id}/networks", method="post", json=body
            ).json()
            net_id = new_net["id"]

        # Else we did find the organization, do nothing
        else:
            print(f"Network '{net_name}' exists in '{org_name}', not recreating")

    # Last, apply new updates to the network. We could have included these in
    # the initial POST as well. Load in the updated data from a JSON file first
    with open("update_net.json", "r") as handle:
        body = json.load(handle)

    # Issue the request and print the feedback
    # TODO consider datadiff or dictdiffer ... current vs intended?
    update_net = req(f"networks/{net_id}", method="put", json=body).json()
    print(f"Current configuration for {net_name}:")
    print(json.dumps(update_net, indent=2))


if __name__ == "__main__":
    # Ensure there are exactly 3 CLI args (file name, org name, net name)
    if len(sys.argv) != 3:
        print("usage: python build_network.py <org_name> <net_name>")
        sys.exit(1)

    # Pass in the arguments into main()
    main(sys.argv[1], sys.argv[2])
