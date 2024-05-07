#!/usr/bin/env bash

echo "Start installing mosaic"
read -p "Enter module name: " modulename
read -p "Enter key name: " keyname
read -p "Enter ip: " ip4
read -p "Enter port: " port

pip install vim poetry npm

# clone this project
git clone https://github.com/mosaicx-org/mosaic-subnet
cd mosaic-subnet

# start virtualenv and enter it
poetry shell

# install dependencies
poetry install

npm install -g pm2

pm2 start "python ~/mosaic_subnet/cli.py --log-level=INFO miner $keyname 0.0.0.0 $port" --name $modulename
comx module register $modulename $keyname --netuid=14 --ip=$ip4 --port=$port
