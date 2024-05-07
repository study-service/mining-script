#!/usr/bin/env bash

echo "Start installing mosaic"
read -p "Enter module name: " modulename
read -p "Enter key name: " keyname
read -p "Enter ip: " ip4
read -p "Enter port: " port

pm2 start "python ~/mosaic_subnet/cli.py --log-level=INFO miner $keyname 0.0.0.0 $port" --name $modulename
comx module update $keyname $modulename $ip4 $port --netuid 14
