#!/bin/bash

# move to folder just in case
cd "${0%/*}"

# update
./updateSelf.sh

# set up the repo inside /etc/
echo "installing to /etc/Scripts/"
if [ -d "/etc/Scripts/"]; then
    rm -rf /etc/Scripts/
fi
sudo cp -r . /etc/Scripts/

echo "setting up service"
rm -f /etc/systemd/system/Scripts.service
sudo cp Scripts.service /etc/systemd/system/
sudo systemctl enable --now Scripts