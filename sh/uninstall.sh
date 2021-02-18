#!/bin/bash

if [ ! -d /usr/local/dchelp ]; then
    echo "dchelp is not installed"
    exit 0
fi

echo "Uninstalling..."
# uninstall dchelp
sudo rm -f /usr/local/bin/dchelp
sudo rm -rf /usr/local/dchelp
sudo rm -rf ~/.cache/dchelp
sudo rm -rf ~/.config/dchelp
echo "Ok"