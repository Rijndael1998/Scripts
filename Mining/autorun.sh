#/bin/bash

cd "${0%/*}"

git pull

./get.sh
screen -dmS xmrig bash -c "./run.sh"
