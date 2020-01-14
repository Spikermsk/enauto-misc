# IOS-XE Model-driven Telemetry using the TIG stack

Run the following scripts in sequence:
```
sudo setup/init.sh
sudo setup/centos7_docker_install.sh
sudo setup/docker_compose_install.sh
sudo setup/install_tig.sh
```

The `install_tig.sh` script modifies the telegraf configuration so that
TCP port 42518 will be used for gRPC telemetry.

Manually update `tig-stack/docker-compose.yml` service `telegraph` to use
the following header (reference in `telegraf_replace.yml`). This ensures
that telegraf is built locally while grafana and influxdb are pulled
from Docker Hub. This also publishes TCP port 42518 on the host so
the managed device can send telemetry data.
```
telegraf:
    # perform local build instead to capture new telegraf config
    build: telegraf
    # expose the gRPC port on telegraf (could use env var, but this is simpler)
    ports: 
        - 42518:42518
```

Start the TIG stack and ensure TCP ports 42518, 3000, 8083, and 8086 are open:
```
sudo docker-compose up --detach
netstat -tna
```

While the stack is booting, test connectivity and reveal
the IP address of the TIG server: `ping tig.njrusmc.net`

Configure the router with some subscriptions:
```
# Enable YANG, otherwise all xpaths will be invalid and subscriptions will fail
netconf-yang

# Configure CPU utilization subscription
telemetry ietf subscription 100
 encoding encode-kvgpb
 filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
 stream yang-push
 update-policy periodic 1000
 receiver ip address 52.71.118.108 42518 protocol grpc-tcp

# Configure memory statistics subscription
telemetry ietf subscription 101
 encoding encode-kvgpb
 filter xpath /memory-ios-xe-oper:memory-statistics/memory-statistic
 stream yang-push
 update-policy periodic 1000
 receiver ip address 52.71.118.108 42518 protocol grpc-tcp
```

Ensure the dial-out connections succeed:
```
CSR1#show telemetry ietf subscription configured brief
  Telemetry subscription brief

  ID               Type        State       Filter type
  --------------------------------------------------------
  100              Configured  Valid       xpath
  101              Configured  Valid       xpath

CSR1#show telemetry ietf subscription 100 receiver 
Telemetry subscription receivers detail:

  Subscription ID: 100
  Address: 52.71.118.108
  Port: 42518
  Protocol: grpc-tcp
  Profile: 
  State: Connected
  Explanation:
  
CSR1#show telemetry ietf subscription 101 receiver 
Telemetry subscription receivers detail:

  Subscription ID: 101
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

Select `add panel` then `add query`

from default (click the metric) and choose your measurement
select field(click the field to view)
alias by: give it a name, "CPU"

add multiple queries for memory stats for free, total, and used memory

click floppy disk icon to save dashboard, and name it

