#!/usr/bin/env bash
# ubuntu 12.04 64x
#
# build litecoind from scratch
#
# v.0.01
# last updated 10/30/2014
#
#

export LC_ALL="en_US.UTF-8"

#----------------------------------------------------------
#required packages
#----------------------------------------------------------
#https://litecoin.info/Compiling_the_Litecoin_daemon_from_source_on_Debian
#apt-get install ntp git build-essential libssl-dev libdb-dev libdb++-dev libboost-all-dev libqrencode-dev

#wget http://miniupnp.free.fr/files/download.php?file=miniupnpc-1.8.tar.gz
#tar -zxf download.php\?file\=miniupnpc-1.8.tar.gz
#cd miniupnpc-1.8/
#make && make install && cd .. && rm -rf miniupnpc-1.8 download.php\?file\=miniupnpc-1.8.tar.gz

apt-get -y update
apt-get install -y git
apt-get install -y wget
apt-get install -y curl
apt-get install -y python-pip

apt-get install -y build-essential
apt-get install -y libtool autotools-dev autoconf
apt-get install -y libssl-dev
apt-get install -y libboost-all-dev

apt-get install -y dh-autoreconf

apt-get install -y ccache
apt-get install -y pkg-config

apt-get install -y  miniupnpc libminiupnpc-dev

homedir=$HOME

#rm -rf $homedir/litecoin

mkdir $homedir/litecoin; cd $homedir/litecoin
git clone git://github.com/litecoin-project/litecoin.git

cd litecoin/src
make -f makefile.unix USE_UPNP=1 USE_QRCODE=1 USE_IPV6=1
strip litecoind; 
