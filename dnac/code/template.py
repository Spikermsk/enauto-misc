#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the template programmer tool on
Cisco DNA center via API calls.
"""

import json
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
    )

    # Build a new project using a name and description
    proj_body = {
        "name": "nickrus_proj",
        "description": "testing some python scripts",
    }
    proj_resp = dnac.req(
        f"dna/intent/api/v1/template-programmer/project", jsonbody=proj_body
    )

    # Wait for the project to get completed, then extract the project ID
    proj_task = dnac.wait_for_task(proj_resp.json()["response"]["taskId"])
    proj_id = proj_task.json()["response"]["data"]

    # Load in the complex template body, then create a template based on it
    with open("template_body.json", "r") as handle:
        temp_body = json.load(handle)
    temp_resp = dnac.req(
        f"dna/intent/api/v1/template-programmer/project/{proj_id}/template",
        jsonbody=temp_body,
    )

    # Wait for task to finish, but don't care about data (only error checks)
    dnac.wait_for_task(temp_resp.json()["response"]["taskId"])


if __name__ == "__main__":
    main()
