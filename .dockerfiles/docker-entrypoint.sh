#!/bin/bash

if [ -d /code ]; then
    pip uninstall -y wildbook-ia
    cd /code && pip install -e ".[tests]"
fi

exec $@
