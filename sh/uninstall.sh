#!/bin/bash

if [ ! -d /usr/local/dchelp ]; then
    echo "dchelp is not installed"
    exit 0
fi

if [[ "$(whoami)" != "root" ]]; then
    echo "Error: permission denied (run this script as root)"
    exit 1
fi

echo "Uninstalling..."
# uninstall dchelp
rm -f /usr/local/bin/dchelp
rm -rf /usr/local/dchelp
rm -rf ~/.cache/dchelp
rm -rf ~/.config/dchelp
echo "Ok"