#!/bin/bash
# Clone the tig-stack repository and change into directory
git clone https://github.com/matisku/tig-stack.git
cd tig-stack/

# Backup original telegraf config template, and copy in custom one,
# which enables Cisco telemetry gRPC on TCP port 42518
mv telegraf/telegraf.template.conf telegraf/telegraf.template.conf.old
cp ~/telegraf.template.conf telegraf/telegraf.template.conf
