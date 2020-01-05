#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple HTTPS server to receive HTTP requests from DNAC
via the eastboard event notification service (webhook).
"""

import json
from flask import Flask, json, request


# Sample username/password to compare to DNAC credentials
USERNAME = "dnacuser"
PASSWORD = "dnacpass"

# Create flask app object
app = Flask(__name__)


@app.route("/dnacwebhook", methods=["POST"])
def process_post():
    """
    Receive POST requests from Cisco DNAC (webhooks). Ensure the
    HTTP basic auth is correct, then simply print the webhook data
    to stdout.
    """

    # Ensure authorization was provided
    auth = request.authorization
    if auth is None:
        msg = f"No username/password provided, check DNA configuration"
        print(msg)
        return (msg, 401)

    # Ensure username and password match
    username = auth.get("username")
    password = auth.get("password")
    if auth is None or username != USERNAME or password != PASSWORD:
        msg = f"Incorrect username/password, check DNA configuration"
        print(msg)
        return (msg, 401)

    # Simply print the data out in pretty JSON format. More professional
    # solutions could write these entries to a remote database
    print(json.dumps(request.data, indent=2))

    # Signal a successful POST back to DNAC (message doesn't matter)
    return ("success", 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
