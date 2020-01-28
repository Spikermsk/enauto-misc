# IOS-XE Model-driven Telemetry using the TIG stack

Run the following scripts in sequence:
```
sudo setup/init.sh
sudo setup/centos7_docker_install.sh
sudo setup/docker_compose_install.sh
sudo setup/install_tig.sh
```

The `install_tig.sh` script clones the forked repository containing
the relevant IOS-XE gRPC changes, starts the TIG stack, and prints
the currently-open TCP ports for verification.

From the router, test connectivity and reveal
the IP address of the TIG server: `ping tig.njrusmc.net`

Use the `make_trees.sh` script, which relies on `pyang`, to build

Configure the router with some subscriptions:
```
# Enable YANG, otherwise all xpaths will be invalid and subscriptions will fail
netconf-yang

# Wait until this command says "netconf-yang: enabled" before continuing.
# If you configure subscriptions too quickly, the xpaths will be inaccessible
do show netconf-yang status

# Configure CPU utilization subscription (periodic 10 seconds)
telemetry ietf subscription 100
 encoding encode-kvgpb
 filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
 stream yang-push
 update-policy periodic 1000
 receiver ip address 10.0.19.188 42518 protocol grpc-tcp

# Configure memory statistics subscription (periodic 10 seconds)
telemetry ietf subscription 101
 encoding encode-kvgpb
 filter xpath /memory-ios-xe-oper:memory-statistics/memory-statistic
 stream yang-push
 update-policy periodic 1000
 receiver ip address 10.0.19.188 42518 protocol grpc-tcp

# Configure CDP neighbor details subscription (on-change)
telemetry ietf subscription 103
 encoding encode-kvgpb
 filter xpath /cdp-ios-xe-oper:cdp-neighbor-details/cdp-neighbor-detail
 stream yang-push
 update-policy on-change
 receiver ip address 10.0.19.188 42518 protocol grpc-tcp
```

Ensure the dial-out connections succeed:
```
CSR1#show telemetry ietf subscription configured brief
  Telemetry subscription brief

  ID               Type        State       Filter type
  --------------------------------------------------------
  100              Configured  Valid       xpath
  101              Configured  Valid       xpath
  102              Configured  Valid       xpath

CSR1#show telemetry ietf subscription 100 receiver 
Telemetry subscription receivers detail:

  Subscription ID: 100
  Address: 52.71.118.108
  Port: 42518
  Protocol: grpc-tcp
  Profile: 
  State: Connected
  Explanation:
```

Browse to Grafana using the default login credentials `admin/admin`
`http://tig.njrusmc.net:3000`

Select `create your first dashboard`

For periodic:

Select `add panel` then `add query`

from default (click mem/cpu metric) and choose your measurement
select field(click the field to view)
alias by: give it a name, "CPU"

add multiple queries for memory stats for free, total, and used memory

click floppy disk icon to save dashboard, and name it


For on-change:

Use a "table" visualization instead

from default (click cdp metric) (can optionally filter on device-id)
select multiple fields:
  * `device_name`
  * `ip_address`
  * `local_intf_name`
  * `port_id` + alias of `remote_intf_name`
optionally group by LIMIT, but can leave blank
format as table

may need to refresh to see changes


A good idea: when building a panel, click the gear (General) and give the
panel a name, like "CPU" or "Memory".

On the main dashboard board, you can "zoom in" by setting a time window
