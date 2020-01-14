# Cisco Meraki for ENAUTO
Postman collection to interact with the Cisco Meraki REST API.

## Usage
Be sure to check the folder descriptions for a summary of each workflow,
and note that each request has at least one "example" showing the response
format. Note that the MV Sense APIs will require physical cameras, something
not currently available in any DevNet sandbox.

## Environments
There are two environments included with the collection:
  * `always_on`: Contains the API key string for the Cisco DevNet
    "Always On" Meraki instance, which is publicly available to all.
  * `reservable`: Contains a sample API key string for the Cisco DevNet
    reservable Meraki instance, which require a DevNet account and
    valid reservation to utilize. This will change with every reservation,
    so be sure to manually update this value for your reservation.

You can add custom environments for your own networks as you see fit.

## Copyright
Copyright 2020 Nicholas Russo.

Consumers may download and edit any document in this collection for personal
use only. Downloading and editing any document in this collection for
redistribution is prohibited.

All rights reserved.
