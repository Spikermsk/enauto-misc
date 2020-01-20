#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using SSH via netmiko to collect data from network devices.
"""

from yaml import safe_load
from netmiko import Netmiko


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:

        # Load the host-specific VRF declarative state
        # with open(f"vars/commands_{host}.yml", "r") as handle:
        with open(f"vars/commands_{host['role']}.yml", "r") as handle:
            commands = safe_load(handle)

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            port=8181,
            username="developer",
            password="C1sco12345",
            device_type="cisco_ios",
        )

        print(f"\nLogged into {conn.find_prompt()} successfully")

        # Iterate over list of commands, issue each one, and print
        # the results
        for command in commands["commands"]:
            result = conn.send_command(command)
            print(f"\n{command}\n{'-' * len(command)}")
            print(result)

        conn.disconnect()


if __name__ == "__main__":
    main()
