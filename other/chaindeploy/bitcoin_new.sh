#!/bin/bash
#building bitcoin v0.11 on ubuntu
#see https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md

export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo add-apt-repository ppa:bitcoin/bitcoin
sudo apt-get update
sudo apt-get install libdb4.8-dev libdb4.8++-dev
sudo apt-get install build-essential libtool autotools-dev autoconf pkg-config libssl-dev libevent-dev bsdmainutils

git clone https://github.com/bitcoin/bitcoin
cd bitcoin
./autogen.sh
./configure
make
make install # optional
