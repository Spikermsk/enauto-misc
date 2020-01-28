#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with Cisco IOS-XE native YANG models to collect
OSPF, key chain, and tunnel configurations relevant to the network.
"""


import xmltodict
from ncclient import manager


def main():
    """
    Execution begins here.
    """

    # Dictionary containing keyword arguments (kwargs) for connecting
    # via NETCONF. Because SSH is the underlying transport, there are
    # several minor options to set up.
    connect_params = {
        "host": "ios-xe-mgmt-latest.cisco.com",
        "port": 10000,
        "username": "developer",
        "password": "C1sco12345",
        "hostkey_verify": False,
        "allow_agent": False,
        "look_for_keys": False,
        "device_params": {"name": "csr"},
    }

    # Unpack the connect_params dict and use them to connect inside
    # of a "with" context manager. The variable "conn" represents the
    # NETCONF connection to the device.
    with manager.connect(**connect_params) as conn:
        print("NETCONF session connected")

        # Craft a relatively complex subtree filter. This allows for granular
        # queries to minimize the data transferred and the load placed on
        # the NETCONF server.
        cfg_filter = """
            <native>
              <interface>
                <Tunnel>
                  <name>100</name>
                </Tunnel>
              </interface>
              <key>
                <chain xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto">
                  <name>KC_OSPF_AUTH</name>
                </chain>
              </key>
              <router>
                <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                  <id>1</id>
                </ospf>
              </router>
            </native>
        """.strip()

        #filter=("xpath", "/routing/routing-instance[name='default']")
        #filter=("xpath", "/routing")
        #filter=("xpath", "/native/key")
        #filter=("xpath", "/native/interface")

        # Execute a "get-config" RPC using the filter defined above
        resp = conn.get_config(source="running", filter=("subtree", cfg_filter))

        # Uncomment line below to see raw RPC XML reply; great for learning
        # print(resp.xml)

        # Parse the XML text into a Python dictionary
        jresp = xmltodict.parse(resp.xml)

        # Uncomment line below to see parsed JSON RPC; great for learning
        import json; print(json.dumps(jresp, indent=2))

    print("NETCONF session disconnected")


if __name__ == "__main__":
    main()
