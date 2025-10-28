#!/bin/bash
echo "Running Black..."
black "$@"
if [ $? -ne 0]; then
    echo "Black failed. Stopping format."
    exit 1
fit
echo "Running iSort"
isort "$@"