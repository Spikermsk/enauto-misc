# Managing and Monitoring Networks using Simple Automation Tools
2 hours, covers network automation fundamentals, builds on DEVASC

## m2: Bootstrapping Network Devices using Day 0 Provisioning Techniques (30m)
1. Course Prerequisites and Business Scenario
2. Utilizing iPXE for Network Device Booting
3. Utilizing ZTP for Initial Device Configuration
4. Scaling and Centralizing Day 0 Operations with Cisco PnP
5. iPXE, ZTP, or PnP; Which is Right for Us?
6. Demo: Writing the ZTP Python Script
7. Demo: Implementing the ZTP Services on a Cisco Router
8. Demo: Standing up new Branch Sites with ZTP
9. Module Summary

## m3: Utilizing Netmiko to Automate Cisco Enterprise Devices (25m)
1. Understanding the Core Network Automation Concepts
2. Demo: Collecting the Initial WAN Health with Netmiko
3. Demo: Configuring OSPF Features with Netmiko via Static Files
4. Assembling Flexible Configuration Templates with Jinja2
5. Demo: Configuring OSPF Features with Netmiko via Jinja2 Templates
6. Demo: Preparing for Network OS Upgrades with Netmiko
7. Module Summary

## m4: Integrating Ansible Playbooks into Network Operations (15m)
1. Introducing Ansible for Network Automation
2. Demo: Ansible Installation and Auxiliary File Creation
3. Demo: Collecting Device State with Ansible
4. Demo: Configuring and Verifying OSPF Features with Ansible
5. Module Summary

## m5: Migrating from CLI-driven to Model-driven Programmability (20m)
1. Network-driven Programmability and YANG Refresher
2. Demo: Exploring YANG models with Cisco DevNet's yangexplorer
3. Demo: Exploring YANG models with Advanced NETCONF Explorer (anx)
4. Planning a Migration from Command-driven to Model-driven Automation
5. Demo: Migrating the Hub Site to NETCONF using Python ncclient
6. Module Summary

## m6: Building a Model-driven Telemetry System using the TIG Stack (30m)
1. Introducing the Telegraf, Influxdb, and Grafana (TIG) Stack
2. Demo: Preparing to Deploy the TIG Stack
3. Demo: Starting a new TIG Stack Container
4. Demo: Exploring the CPU and CDP Operational YANG Models
5. Demo: Configuring gRPC Dial-out Connections via CLI
6. Demo: Creating new Dashboard Visualizations in Grafana
7. Course Summary and Homework Challenges
  - after migration, have them finish it by migrating the spokes too
  - add new dial-out connections using netmiko
  - add a new visualization for OSPF state 
