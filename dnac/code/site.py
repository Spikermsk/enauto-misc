#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the site API (health) on
Cisco DNA center via API calls.
"""

import json
import time
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="sandboxdnac2.cisco.com", username="devnetuser", password="Cisco123!", verify=False
    )

    # API requires specifying the epoch as query parameter. Take current
    # time in epoch seconds, convert to ms, and remove decimal
    # Note: epoch 0 = 00:00:00 UTC on 1 January 1970
    current_epoch = int(time.time() * 1000)
    params = {"timestamp": current_epoch}

    site_health = dnac.req(
        f"dna/system/api/v1/site-health",
        params=params,
    )

    site_data = site_health.json()["response"]
    for site in site_data:
        trimmed = {k: v for k, v in site.items() if v is not None}
        print(json.dumps(trimmed, indent=2))


if __name__ == "__main__":
    main()
