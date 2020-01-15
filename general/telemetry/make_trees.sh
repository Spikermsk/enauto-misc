#/bin/bash
# Small script to avoid typing these long commands
# Clone this repo to access to latest YANG models:
# https://github.com/YangModels

# Build tree for Cisco XE 16.12.1 Cisco native CPU stats
pyang --format tree --path ~/code/yang/vendor/cisco/xe/16121 \
  --output data_ref/cpu_oper.txt \
  ~/code/yang/vendor/cisco/xe/16121/Cisco-IOS-XE-process-cpu-oper.yang

# Build tree for Cisco XE 16.12.1 Cisco native memory stats
pyang --format tree --path ~/code/yang/vendor/cisco/xe/16121 \
  --output data_ref/mem_oper.txt \
  ~/code/yang/vendor/cisco/xe/16121/Cisco-IOS-XE-memory-oper.yang

# Build tree for Cisco XE 16.12.1 Cisco native CDP stats
pyang --format tree --path ~/code/yang/vendor/cisco/xe/16121 \
  --output data_ref/cdp_oper.txt \
  ~/code/yang/vendor/cisco/xe/16121/Cisco-IOS-XE-cdp-oper.yang
