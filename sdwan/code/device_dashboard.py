#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
and test its Device Dashboard API methods.
"""

from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN(
        # host="sandboxsdwan.cisco.com",
        host="10.10.20.90",
        port=8443,
        # username="devnetuser",
        username="admin",
        # password="Cisco123!",
        password="admin",
    )

    api_calls = [
        sdwan.get_device_top_applications,
        sdwan.get_device_system_summary,
    ]
    CiscoSDWAN.run_api_calls(api_calls, filepath="current")


if __name__ == "__main__":
    main()
