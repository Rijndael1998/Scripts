#!/bin/bash

cd "${0%/*}"

echo "installing deps"
./installDeps.sh

rm PKGBUILD
echo "piggy backing off the aur"
curl https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=xmrig-donateless > PKGBUILD
source PKGBUILD

rm xmrig.tar.gz
echo "getting xmrig"
wget -O xmrig.tar.gz $source
echo "$sha256sums xmrig.tar.gz" | sha256sum --check
# TODO: fail if it doesn't pass

echo "extracting"
rm -r xmrig
mkdir xmrig
tar -xf xmrig.tar.gz -C xmrig

wd=$(pwd)

echo "building"
cd $wd/xmrig/
prepare
cd $wd/xmrig/
build

cd $wd
