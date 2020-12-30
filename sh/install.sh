#!/bin/bash
# dchelp install script

if [ -d /usr/local/dchelp ]; then
    echo "dchelp is already installed"
    exit 0
fi

fail=0

if [[ "$(whoami)" != "root" ]]; then
    echo "Error: permission denied (run this script as root)"
    fail=$((fail + 1))
elif [[ "$(uname)" != "Linux" ]]; then
    echo "Error: dchelp works only on Linux"
    fail=$((fail + 1))
elif [[ "$(which python)" == "" ]]; then
    echo "Error: python is not installed"
    fail=$((fail + 1))
elif [[ "$(which docker)" == "" ]]; then
    echo "Error: docker is not installed"
    fail=$((fail + 1))
elif [[ "$(which docker-compose)" == "" ]]; then
    echo "Error: docker-compose is not installed"
    fail=$((fail + 1))
fi

if [[ $fail > 0 ]]; then
    exit 1
fi

echo "Installing..."
cp -r ./dchelp /usr/local/dchelp
cp ./sh/dchelp /usr/local/bin/dchelp
echo "OK"