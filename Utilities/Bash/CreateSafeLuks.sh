#!/bin/bash
cryptsetup -y -v --type luks2 --iter-time 20000 --pbkdf argon2id luksFormat $1
