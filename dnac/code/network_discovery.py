#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the network discovery tool on
Cisco DNA center via API calls.
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
        host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
    )

    cred_list = []
    cred_types = ["CLI", "SNMPV2_READ_COMMUNITY", "SNMPV2_WRITE_COMMUNITY"]
    for cred in cred_types:
        cred_resp = dnac.req("dna/intent/api/v1/global-credential", params={"credentialSubType": cred})
        cred_list.append(cred_resp.json()["response"][0]["id"])

    with open("discoveries.json", "r") as handle:
        discoveries = json.load(handle)
    for disc_body in discoveries:
        disc_body["globalCredentialIdList"] = cred_list
        run_discovery(dnac, disc_body)

def run_discovery(dnac, disc_body):

    disc_resp = dnac.req("dna/intent/api/v1/discovery", method="post", jsonbody=disc_body)

    # Wait for async job to complete
    disc_task = dnac.wait_for_task(disc_resp.json()["response"]["taskId"])
    disc_id = disc_task.json()["response"]["progress"]

    success = False
    for x in range(120):
        get_disc = dnac.req(f"dna/intent/api/v1/discovery/{disc_id}")
        data = get_disc.json()["response"]
        if data["discoveryCondition"].lower() != "complete":
            print(f"Discovery {disc_id} status: {data['discoveryCondition']}")
            time.sleep(5)
        else:
            print(f"Discovery {disc_id} found {data['numDevices']} devices")
            success = True
            break

    if not success:
        raise TimeoutError("Discovery did not complete in time")

    file_dir = f"discovered_devices/{disc_id}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    dev_sum = dnac.req(f"dna/intent/api/v1/discovery/{disc_id}/network-device")
    for dev in dev_sum.json()["response"]:
        if dev['reachabilityStatus'].lower() == "success":
            print(f"{dev['hostname']} success")
            if dev['inventoryCollectionStatus'].lower() == "managed":
                get_dev = dnac.req(f"dna/intent/api/v1/network-device/{dev['id']}")
                output = {
                    "discovery": dev,
                    "device": get_dev.json()["response"]
                }
                with open(f"{file_dir}/{dev['hostname']}.json", "w") as handle:
                    json.dump(output, handle, indent=2)
        else:
            print(f"{dev['managementIpAddress']} failed: {dev['reachabilityFailureReason']}")


if __name__ == "__main__":
    main()
