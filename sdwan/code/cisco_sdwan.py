#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco SD-WAN to simplify
API interactions.
"""

import time
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
            host="10.10.20.90", port=8443, username="admin", password="admin"
        )

    def _req(self, resource, method="get", params=None, jsonbody=None):
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
            json=jsonbody,
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
            return self._req(
                "statistics/dpi/aggregation", method="post", jsonbody=query
            )

        return self._req("statistics/dpi/aggregation")

    def get_device_system_summary(self, query=None):
        """
        Display historical memory and CPU information about the device.
        Use a GET request if query is not specified to collect all data.
        Use a POST request if query is specified to collect data subsets.
        """

        if query:
            return self._req("statistics/system", method="post", jsonbody=query)

        return self._req("dataservice/statistics/system")

    #
    # Real-time monitoring APIs
    #

    def get_device_approute_statistics(self, device_id):
        return self._req(
            "dataservice/device/app-route/statistics",
            params={"deviceId": device_id},
        )

    def get_device_tunnel_statistics(self, device_id):
        return self._req(
            "dataservice/device/tunnel/statistics", params={"deviceId": device_id}
        )

    def get_device_control_connections(self, device_id):
        return self._req(
            "dataservice/device/control/connections", params={"deviceId": device_id}
        )

    def get_feature_templates(self):
        return self._req("dataservice/template/feature")

    def add_fd_vsmart_device_template(self):
        """
        Combine the required factory default feature templates into
        a vSmart template. this includes AAA, security, system, OMP,
        VPN 0, and VPN 512.
        """

        all_temps = self.get_feature_templates()
        fd_temps = []
        for temp in all_temps.json()["data"]:
            temp_type = temp["templateType"].lower()
            if temp["factoryDefault"] and (
                temp_type.endswith("vsmart") or temp_type == "aaa"
            ):
                fd_temps.append(
                    {
                        "templateId": temp["templateId"],
                        "templateType": temp["templateType"],
                    }
                )

        body = {
            "templateName": "Basic_template",
            "templateDescription": "Collection of default templates",
            "deviceType": "vsmart",
            "configType": "template",
            "factoryDefault": False,
            "policyId": "",
            "featureTemplateUidRange": [],
            "generalTemplates": fd_temps,
        }
        add_temp = self._req(
            "dataservice/template/device/feature", method="post", jsonbody=body
        )
        return add_temp

    def get_devices(self):
        """
        Returns a list of all SD-WAN devices.
        """
        return self._req("dataservice/device")

    def attach_vsmart_device_template(self, template_id, var_map):
        """
        Given an existing template and supplied variables, attaches
        the vSmart template to all discovered vSmart instances.
        The var_map uses hostnames as keys and a 2-tuple as the value,
        containing the site ID and default gateway IP address as strings:
          var_map = {"vsmart-01": ("100", "10.10.20.254")}
        """
        devices = self.get_devices()
        vsmarts = []
        for dev in devices.json()["data"]:
            if dev["device-model"].lower() == "vsmart":
                site_id, def_gway = var_map[dev["host-name"]]
                vsmart_dict = {
                    "csv-status": "complete",
                    "csv-deviceId": dev["uuid"],
                    "csv-deviceIP": dev["system-ip"],
                    "csv-host-name": dev["host-name"],
                    "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/address": def_gway,
                    "//system/host-name": dev["host-name"],
                    "//system/system-ip": dev["system-ip"],
                    "//system/site-id": site_id,
                    "csv-templateId": template_id,
                }
                vsmarts.append(vsmart_dict)

        body = {
            "deviceTemplateList": [
                {
                    "templateId": template_id,
                    "device": vsmarts,
                    "isEdited": False,
                    "isMasterEdited": False,
                }
            ]
        }
        attach_resp = self._req(
            "dataservice/template/device/config/attachfeature",
            method="post",
            jsonbody=body,
        )

        attach_id = attach_resp.json()["id"]
        return self._wait_for_device_action_done(attach_id)

    def _add_policy(self, obj_type, name, entries):
        body = {
            "name": name,
            "description": "Desc Not Required",
            "type": obj_type,
            "entries": entries,
        }
        return self._req(
            f"dataservice/template/policy/list/{obj_type}",
            method="post",
            jsonbody=body,
        )

    def add_policy_site(self, name, site_list):
        entries = [{"siteId": str(site)} for site in site_list]
        return self._add_policy("site", name, entries)

    def add_policy_vpn(self, name, vpn_list):
        entries = [{"vpn": str(vpn)} for vpn in vpn_list]
        return self._add_policy("vpn", name, entries)

    def add_policy_sla(self, name, sla_entries):
        return self._add_policy("sla", name, sla_entries)

    def add_policy_mesh(self, name, vpn_id, region_map, description="none"):
        regions = []
        for name, site_id in region_map.items():
            regions.append({"name": name, "siteLists": site_id})

        body = {
            "name": name,
            "type": "mesh",
            "description": description,
            "definition": {"vpnList": vpn_id, "regions": regions},
        }

        return self._req(
            f"dataservice/template/policy/definition/mesh",
            method="post",
            jsonbody=body,
        )

    def add_policy_approute_dscp(
        self, name, sla_id, dscp_dec, color, description="none"
    ):
        body = {
            "name": name,
            "type": "appRoute",
            "description": description,
            "sequences": [
                {
                    "sequenceId": 1,
                    "sequenceName": "App Route",
                    "sequenceType": "appRoute",
                    "match": {
                        "entries": [{"field": "dscp", "value": str(dscp_dec)}]
                    },
                    "actions": [
                        {
                            "type": "slaClass",
                            "parameter": [
                                {"field": "name", "ref": sla_id},
                                {"field": "preferredColor", "value": color},
                            ],
                        }
                    ],
                }
            ],
        }
        return self._req(
            f"dataservice/template/policy/definition/approute",
            method="post",
            jsonbody=body,
        )

    def get_policy_vsmart(self):
        return self._req(f"dataservice/template/policy/vsmart")

    def add_policy_vsmart(
        self, name, sites, vpns, approute_id, mesh_id, description="none"
    ):
        body = {
            "policyDescription": description,
            "policyType": "feature",
            "policyName": name,
            "policyDefinition": {
                "assembly": [
                    {
                        "definitionId": approute_id,
                        "type": "appRoute",
                        "entries": [{"siteLists": sites, "vpnLists": vpns}],
                    },
                    {"definitionId": mesh_id, "type": "mesh"},
                ]
            },
            "isPolicyActivated": False,
        }

        # No response body
        self._req(
            f"dataservice/template/policy/vsmart", method="post", jsonbody=body
        )
        policies = self._req(f"dataservice/template/policy/vsmart")
        for policy in policies.json()["data"]:
            if policy["policyName"] == name:
                return policy
        return {"policyId": None}

    def activate_policy_vsmart(self, policy_id):
        activate_resp = self._req(
            f"dataservice/template/policy/vsmart/activate/{policy_id}",
            method="post",
            params={"confirm": "true"},
            jsonbody={},
        )

        activate_id = activate_resp.json()["id"]
        return self._wait_for_device_action_done(activate_id)

    def _wait_for_device_action_done(self, uuid, interval=20):
        while True:
            time.sleep(interval)
            check = self._req(f"dataservice/device/action/status/{uuid}")
            if check.json()["summary"]["status"].lower() != "in_progress":
                break
        return check
