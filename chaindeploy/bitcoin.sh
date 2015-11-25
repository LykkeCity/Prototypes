#!/usr/bin/env bash
# bitcoind linux buildscript for a fresh ubuntu 12.04 64x machine
# to use: make sure .sh is executable with chmod +x, then ./bitcoin.sh
#
# v.0.2
# updated 8/1/2014
# updated 24/2/2015

export LC_ALL="en_US.UTF-8"

#----------------------------------------------------------
# required packages
#----------------------------------------------------------

sudo apt-get -y update
sudo apt-get install -y git wget curl python-pip
sudo apt-get install -y build-essential
sudo apt-get install -y libtool autotools-dev autoconf
sudo apt-get install -y libssl-dev
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y dh-autoreconf
sudo apt-get install -y ccache pkg-config



#Berkeley DB always makes problems

sudo apt-get install -y libdb++-dev

#sudo apt-get install -y libdb4.8-dev
#sudo apt-get install -y libdb4.8++
#sudo apt-get install -y libdb4.++-dev


homedir=$HOME

#----------------------------------------------------------
# Build berkley db4.8 NC
#----------------------------------------------------------

#cd $homedir

#mkdir BDB && cd BDB

#sudo apt-get install python-software-properties

#if [ ! -e db-4.8.30 ]
#then
#wget http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
#tar zxvf db-4.8.30.NC.tar.gz
#rm -f db-4.8.30.NC.tar.gz
#fi

#cd db-4.8.30.NC/build_unix
#sudo ../dist/configure --prefix=/usr/local --enable-cxx
#make
#sudo make install

#sudo ln -s /usr/local/BerkeleyDB.4.8/lib/libdb_cxx-4.8.so /usr/lib/libdb_cxx-4.8.so

#cd $HOME/BDB
#rm -fr db-4.8.30/


#sudo apt-get install -y libboost1.37-dev #not needed

#apt-get install -y libprotobuf-dev
#apt-get install -y alien

#----------------------------------------------------------
# build bitcoin from source
#----------------------------------------------------------

rm -rf $homedir/bitcoin
mkdir $homedir/bitcoin; cd $homedir/bitcoin
git clone git://github.com/bitcoin/bitcoin.git $homedir/bitcoin
git checkout 0.10.0

/bin/bash $homedir/bitcoin/autogen.sh

#build without QT
cd $homedir/bitcoin && ./configure --without-qt --with-incompatible-bdb
sudo make
