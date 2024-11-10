#!/bin/sh

curl -X POST http://core-s1:30900/api/v1/query -d 'query=vmware_vm_power_state{instance=~"192.168.100.35:3270.*"}'