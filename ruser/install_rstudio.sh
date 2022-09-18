#!/usr/bin/sh
apt-get -yqq update

# install RStudio Server
wget https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.4.1106-amd64.deb
gdebi --n rstudio-server-1.4.1106-amd64.deb
rm rstudio-server-1.4.1106-amd64.deb
export LANG="en_US"

apt-get -qq purge
apt-get -qq clean
rm -rf /var/lib/apt/lists/*
