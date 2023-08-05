#!/bin/bash

# Run tests.

cat <<EOF
# `whoami`@`hostname`:$PWD$ runtests.sh $@
EOF

set -e

export BASE_SETTINGS_MODULE=test
export FORCE_SETUP_POSTGRES_DATABASE=1
export PGDATABASE=test_icekit
export REUSE_DB=1
export SRC_PGDATABASE="$ICEKIT_DIR/initial_data.sql"

exec entrypoint.sh python "$ICEKIT_DIR/bin/manage.py" test --noinput --verbosity=2 "$@"
