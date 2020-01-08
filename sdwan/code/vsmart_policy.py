#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
and add a new vSmart device template.
"""

from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()

    # Create the policy objects relevant for our test policy, and store
    # their listId attributes to reference later
    site_id = sdwan.add_policy_site("WestUS", [200, 300]).json()["listId"]
    print(f"Created site with ID {site_id}")

    vpn_id = sdwan.add_policy_vpn("Engineering", [1]).json()["listId"]
    print(f"Created VPN with ID {vpn_id}")

    sla_id = sdwan.add_policy_sla(
        "Voice", [{"latency": "150", "loss": "1", "jitter": "30"}]
    ).json()["listId"]
    print(f"Created SLA class with ID {sla_id}")

    mesh_id = sdwan.add_policy_mesh(
        "EngMesh", vpn_id, {"EngWest": [site_id]}
    ).json()["definitionId"]
    print(f"Created mesh network with ID {mesh_id}")

    approute_id = sdwan.add_policy_approute_dscp(
        "VoiceMPLS",
        sla_id,
        46,
        "mpls",
        description="Voice DSCP 46 should prefer MPLS",
    ).json()["definitionId"]
    print(f"Created voice-over-mpls approute with ID {approute_id}")

    policy_id = sdwan.add_policy_vsmart(
        "EngPolicy", [site_id], [vpn_id], approute_id, mesh_id
    )["policyId"]
    print(f"Created vsmart policy with ID {policy_id}")

    activate_resp = sdwan.activate_policy_vsmart(policy_id)

    # check for success
    data = activate_resp.json()
    status = data["summary"]["status"]
    print(f"vSmart policy activation status: {status}")


if __name__ == "__main__":
    main()
