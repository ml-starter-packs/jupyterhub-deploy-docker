#!/usr/bin/sh
apt-get -yqq update

# install R
apt-get -y install r-base r-base-dev
R CMD javareconf

apt-get -qq purge
apt-get -qq clean
rm -rf /var/lib/apt/lists/*
