#!/bin/bash

# move to folder
cd "${0%/*}"

# get repo if doesn't exist
if [ ! -d "Website-Neo" ]; then
    git clone https://github.com/Rijndael1998/Website-Neo
fi

cd Website-Neo

# making sure repo is clean
git fetch --all
git reset --hard origin/main

# building and running repo
yarn install
yarn run build
yarn run start -p 10000
