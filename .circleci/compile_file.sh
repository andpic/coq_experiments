#!/bin/bash

COQ_FILE="$1"
FILE_NAME="${COQ_FILE%.*}"

echo -n "Compiling ${COQ_FILE}... "

coqc $COQ_FILE
if [ ! -f "${FILE_NAME}.vo" ]; then
    echo "FAIL"
    exit -1
else
    echo "SUCCESS"
fi