#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the various health URLs
on Cisco DNA center via API calls.
"""

import json
import time
import os
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="sandboxdnac2.cisco.com",
        username="devnetuser",
        password="Cisco123!",
        verify=False,
    )

    health_dir = "health_ref"
    if not os.path.exists(health_dir):
        os.makedirs(health_dir)

    # API requires specifying the epoch as query parameter. Take current
    # time in epoch seconds, convert to ms, and remove decimal
    # Note: epoch 0 = 00:00:00 UTC on 1 January 1970
    current_epoch = int(time.time() * 1000)
    params = {"timestamp": current_epoch}

    for health in ["network", "site", "client"]:
        health_resp = dnac.req(f"dna/intent/api/v1/{health}-health", params=params)

        with open(f"{health_dir}/get_{health}_health.json", "w") as handle:
            json.dump(health_resp.json(), handle, indent=2)
        print(f"Wrote {health} health to disk")


if __name__ == "__main__":
    main()
