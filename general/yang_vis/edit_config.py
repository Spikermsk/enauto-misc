#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with Openconfig YANG models to manage Ethernet
VLANs on a Cisco NX-OS switch via the always-on Cisco DevNet sandbox.
"""


import xmltodict
import yaml
from lxml.etree import fromstring
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

        # Perform the update, and if success, print a message
        config_resp = update_wan(conn, "config_state.yml")

        # If config and save operations succeed, print "saved" message
        if config_resp.ok and save_config_iosxe(conn).ok:
            print("Successfully saved running-config to startup-config")

    print("NETCONF session disconnected")


def update_wan(conn, filename):
    """
    Updates switchports with new config based on YAML file. Expects that the
    NETCONF connection is already open and that all data is valid. Feel
    free to add more data validation here as a challenge.
    """

    with open(filename, "r") as handle:
        data = yaml.safe_load(handle)

    payload = {
        "config": {
            "native": {
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
                "interface": {
                    "Tunnel": {
                        "name": "100",
                        "ip": {
                            "ospf": {
                                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf",
                                "authentication": {
                                    "key-chain": {"name": data["security"]["key_chain"]["name"]}
                                }
                            }
                        }
                    }
                },
                "key": {
                    "chain": {
                        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-crypto",
                        "name": data["security"]["key_chain"]["name"],
                        "key": {
                            "id": data["security"]["key_chain"]["key"]["id"],
                            "cryptographic-algorithm": "hmac-sha-256",
                            "key-string": {"key": data["security"]["key_chain"]["key"]["text"]},
                        }
                    }
                },
                "router": {
                    "ospf": {
                        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf",
                        "id": "1",
                        "auto-cost": {"reference-bandwidth": data["routing"]["ref_bw"]},
                        "passive-interface": {"interface": ["Loopback0"]},
                        "ttl-security": {
                            "all-interfaces": None,
                            "hops": data["routing"]["ttl_security_hops"],
                        }
                    }
                }
            }
        }
    }

    # Assemble the XML payload by "unparsing" the JSON dict (JSON --> XML)
    xpayload = xmltodict.unparse(payload)
    config_resp = conn.edit_config(target="running", config=xpayload)
    return config_resp


def save_config_iosxe(conn):
    """
    Save config on Cisco IOS-XE is complex and requires a custom RPC.
    Reference the IOS-XE programmability documentation for further details.
    """

    save_rpc = '<save-config xmlns="http://cisco.com/yang/cisco-ia"/>'
    save_resp = conn.dispatch(fromstring(save_rpc))
    return save_resp


if __name__ == "__main__":
    main()
