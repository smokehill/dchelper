#!/bin/bash

if [ -d /usr/local/dchelp ]; then
    echo "dchelp is already installed"
    exit 0
fi

if [[ "$(uname)" != "Linux" ]]; then
    echo "Error: dchelp works only on Linux"
    exit 1
fi

if [[ "$(whoami)" != "root" ]]; then
    echo "Error: permission denied (run this script as root)"
    exit 1
fi

fail=0

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
# install dchelp
cp -r ./dchelp /usr/local/dchelp
touch /usr/local/bin/dchelp
chmod +x /usr/local/bin/dchelp
cat > /usr/local/bin/dchelp << EOF
#!/bin/bash

if [ ! -d ~/.cache/dchelp ]; then
    mkdir ~/.cache/dchelp
    chmod 775 ~/.cache/dchelp
fi

if [ ! -d ~/.config/dchelp ]; then
    mkdir ~/.config/dchelp
    chmod 775 ~/.config/dchelp
    touch ~/.config/dchelp/data.json
    chmod 775 ~/.config/dchelp/data.json
    echo "[]" >> ~/.config/dchelp/data.json
fi

$(which python) /usr/local/dchelp/main.py \$*
EOF
echo "Ok"