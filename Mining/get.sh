#!/bin/bash

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
mkdir xmrig
tar -xf xmrig.tar.gz -C xmrig
rm -r xmrig

echo "building"
cd xmrig/
prepare
cd ../
build

cd ../
