#!/bin/bash
# dchelp install script

if [ -d /usr/local/dchelp ]; then
    echo "dchelp is already installed"
    exit 0
fi

fail=0

if [[ "$(whoami)" != "root" ]]; then
    fail=$((fail + 1))
    echo "Error: permission denied (run this script as root)"
fi

if [[ "$(uname)" != "Linux" ]]; then
    fail=$((fail + 1))
    echo "Error: dchelp works only on Linux"
fi

if [[ "$(which python)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: python not found"
fi

if [[ "$(which docker)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: docker not found"
fi

if [[ "$(which docker-compose)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: docker-compose not found"
fi

if [[ $fail > 0 ]]; then
    exit 1
fi

echo "Installing..."
cp -r ./dchelp /usr/local/dchelp
cp ./sh/dchelp /usr/local/bin/dchelp
echo "Ok"