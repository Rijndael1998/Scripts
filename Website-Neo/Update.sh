# making sure repo is clean
git fetch --all
git reset --hard origin/main

# building and running repo
yarn install
yarn run build
