#!/bin/bash

# Install Node modules, Bower components and Python requirements, setup
# database, apply migrations, and execute command.

cat <<EOF
# `whoami`@`hostname`:$PWD$ entrypoint.sh $@
EOF

set -e

# Make sure this is set, even if to an empty string, to stop Supervisor from
# complaining.
export EXTRA_SUPERVISORD_CONFIG="$EXTRA_SUPERVISORD_CONFIG"

# Add bin directories to PATH if not already there.
# See: http://superuser.com/a/39995
if [[ ":$PATH:" != *":$ICEKIT_DIR/bin:"* ]]; then
    export PATH="$ICEKIT_DIR/bin${PATH:+:$PATH}"
fi
if [[ ":$PATH:" != *":$ICEKIT_PROJECT_DIR/venv/bin:"* ]]; then
    export PATH="$ICEKIT_PROJECT_DIR/venv/bin${PATH:+:$PATH}"
fi

# Configure Python.
export PIP_DISABLE_PIP_VERSION_CHECK=on
export PYTHONHASHSEED=random
export PYTHONWARNINGS=ignore

# Get number of CPU cores, so we know how many processes to run.
export CPU_CORES=$(python -c 'import multiprocessing; print multiprocessing.cpu_count();')

# Get project name from the project directory.
export ICEKIT_PROJECT_NAME=$(basename "$ICEKIT_PROJECT_DIR")

# Install Node modules.
waitlock.sh npm-install.sh "$ICEKIT_DIR"
waitlock.sh npm-install.sh "$ICEKIT_PROJECT_DIR"

# Install Bower components.
waitlock.sh bower-install.sh "$ICEKIT_DIR"
waitlock.sh bower-install.sh "$ICEKIT_PROJECT_DIR"

# Install Python requirements.
waitlock.sh pip-install.sh "$ICEKIT_DIR"
waitlock.sh pip-install.sh "$ICEKIT_PROJECT_DIR"

# Setup database.
source setup-postgres-env.sh
waitlock.sh setup-postgres-database.sh

# Apply migrations.
waitlock.sh migrate.sh "$ICEKIT_PROJECT_DIR/var"

# Open a new shell by default, so we can interactively execute commands with
# the correct environment.
exec "${@:-bash}"
