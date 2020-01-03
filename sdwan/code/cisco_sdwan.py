#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco SD-WAN to simplify
API interactions.
"""

import json
import requests


class CiscoSDWAN:
    """
    A simple Cisco SD-WAN SDK to demonstrate API interaction.
    """

    def __init__(self, host, port, username, password):
        """
        Constructor that creates the long-lived HTTP session and
        performs the initial login.
        """
        self.base_url = f"https://{host}:{port}"
        login_creds = {"j_username": username, "j_password": password}
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        requests.packages.urllib3.disable_warnings()
        self.session = requests.session()
        auth_resp = self.session.post(
            f"{self.base_url}/j_security_check",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=login_creds,
            verify=False,
        )
        auth_resp.raise_for_status()

        # URL almost always returns 200, even upon failure. If any
        # body text is present, that is a failure, likely a credentials issue
        if auth_resp.text:
            auth_resp.status_code = 401
            auth_resp.reason = "UNAUTHORIZED; check username/password"
            auth_resp.raise_for_status()

    @staticmethod
    def run_api_calls(api_calls, filepath="data_ref"):
        """
        Helper function to iterate over a list of API
        calls and run them. Only works when there are no
        arguments being passed into each API wrapper call
        (mostly for getters).
        """
        for api_call in api_calls:
            resp = api_call()
            name = api_call.__name__
            print(f"Executing '{name}' API call")
            with open(f"{filepath}/{name}.json", "w") as handle:
                json.dump(resp.json(), handle, indent=2)

    @staticmethod
    def get_instance_always_on():
        """
        Factory-style function that retusn a new CiscoSDWAN object
        connected to the DevNet SDWAN Always-On sandbox.
        """
        return CiscoSDWAN(
            host="sandboxsdwan.cisco.com",
            port=8443,
            username="devnetuser",
            password="Cisco123!",
        )

    @staticmethod
    def get_instance_reserved():
        """
        Factory-style function that retusn a new CiscoSDWAN object
        connected to the DevNet SDWAN Reserved sandbox.
        """
        return CiscoSDWAN(
            host="10.10.20.90",
            port=8443,
            username="admin",
            password="admin",
        )

    def _req(self, resource, method="get", params=None, json=None):
        """
        Internal helper function to issue requests and raise errors
        if the request fails. Returns the entire response object
        on success.
        """
        resp = self.session.request(
            method=method,
            url=f"{self.base_url}/{resource}",
            headers=self.headers,
            params=params,
            json=json,
        )
        resp.raise_for_status()
        return resp

    #
    # Device Inventory APIs
    #

    def get_all_devices(self, model=None):
        """
        Display all Viptela devices in the overlay network that are
        connected to the vManage NMS.
        """
        params = {"model": model} if model else None
        return self._req("dataservice/device", params=params)

    def get_device_controllers(self, model=None):
        """
        Display all available controllers—vBond orchestrators,
        vManage NMS, and vSmart controllers—in the overlay network.
        """
        params = {"model": model} if model else None
        return self._req("dataservice/system/device/controllers", params=params)

    def get_device_vedges(self, model=None):
        """
        Display all available vEdge routers in the overlay network.
        """
        params = {"model": model} if model else None
        return self._req("dataservice/system/device/vedges", params=params)

    #
    # Dashboard APIs
    #

    def get_aar_routing(self, metric, limit=None):
        """
        Display application-aware routing information.
        """
        raise NotImplementedError("something is wrong")
        params = {"limit": limit} if limit else None
        return self._req(f"dataservice/tunnels/summary/{metric}", params=params)

    def get_alarm_count(self):
        """
        Display a count of active and cleared alarms.
        """
        return self._req("dataservice/alarms/count")

    def get_certificate_summary(self):
        """
        Display information about certificates.
        """
        return self._req("dataservice/certificate/stats/summary")

    def get_control_status(self):
        """
        Display information about the status of control connections.
        """
        return self._req("dataservice/device/control/count")

    #
    # Device Dashboard APIs
    #

    def get_device_top_applications(self, query=None):
        """
        Display applications with the highest utilization for a device.
        Use a GET request if query is not specified to collect all data.
        Use a POST request if query is specified to collect data subsets.
        """

        if query:
            return self._req("statistics/dpi/aggregation", method="post", json=query)

        return self._req("statistics/dpi/aggregation")

    def get_device_system_summary(self, query=None):
        """
        Display historical memory and CPU information about the device.
        Use a GET request if query is not specified to collect all data.
        Use a POST request if query is specified to collect data subsets.
        """

        if query:
            return self._req("statistics/system", method="post", json=query)

        return self._req("dataservice/statistics/system")

    #
    # Real-time monitoring APIs
    #

    def get_device_approute_statistics(self, device_id):
        return self._req("dataservice/device/app-route/statistics", params={"deviceId": device_id})
        
    def get_device_tunnel_statistics(self, device_id):
        return self._req("dataservice/device/tunnel/statistics", params={"deviceId": device_id})

    def get_device_control_connections(self, device_id):
        return self._req("dataservice/device/control/connections", params={"deviceId": device_id})
