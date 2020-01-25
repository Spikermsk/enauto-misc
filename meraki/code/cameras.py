#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to collect video
footage from MV sense cameras.
"""

import sys
import json
import requests
from meraki_helpers import get_network_id, req


def main(org_name, net_name):
    """
    Execution begins here.
    """

    net_id = get_network_id(net_name, org_name)

    cameras = req(f"networks/{net_id}/devices").json()
    # Print the list of cameras collected
    print(json.dumps(cameras, indent=2))

    for camera in cameras:
        sn = camera["serial"]
        video_link = req(f"networks/{net_id}/cameras/{sn}/videoLink").json()

        # Print the retrieved video link response
        print(json.dumps(video_link, indent=2))
        print(f"Video link for camera {sn}:\n{video_link['url']}")

        timestamp = None
        if timestamp:
            params = {"timestamp": timestamp}
        else:
            params = None

        snapshot_link = req(
            f"networks/{net_id}/cameras/{sn}/snapshot",
            method="post",
            params=params,
        ).json()

        # Print the retrieved snapshot link response
        print(json.dumps(snapshot_link, indent=2))

        import pdb; pdb.set_trace()
        image = requests.get(
            snapshot_link["url"],
            headers={
                "User-Agent": "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Firefox/41.0"
            },
        )
        image.raise_for_status()

        with open(f"camera_snapshots/{sn}.jpg", "wb") as handle:
            handle.write(image.content)

        print(f"Snapshot for camera {sn} saved")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python splash.py <org_name> <net_name>")
        sys.exit(1)

    # Pass in the arguments into main()
    main(sys.argv[1], sys.argv[2])
    # python cameras.py "Loop Free Consulting" "Home Camera"
