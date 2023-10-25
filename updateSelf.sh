#!/bin/bash

echo id: $(id)

# move to folder just in case
cd "${0%/*}"

# making sure repo is clean
git fetch --all
git reset --hard origin/main

