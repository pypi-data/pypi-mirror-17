#!/bin/bash

# Install Node modules in the given directory, if they have changed.

cat <<EOF
# `whoami`@`hostname`:$PWD$ npm-install.sh $@
EOF

set -e

DIR="${1:-$PWD}"

mkdir -p "$DIR"
cd "$DIR"

if [[ ! -s package.json ]]; then
    cat <<EOF > package.json
{
  "name": "icekit-project",
  "dependencies": {
  },
  "private": true
}
EOF
fi

touch package.json.md5

if [[ ! -s package.json.md5 ]] || ! md5sum --status -c package.json.md5 > /dev/null 2>&1; then
    echo "Node modules in '$DIR' directory are out of date."
    npm install
    md5sum package.json > package.json.md5
fi
