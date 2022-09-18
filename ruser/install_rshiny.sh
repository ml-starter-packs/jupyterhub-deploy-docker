#!/usr/bin/sh
# install Shiny Server
wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.16.958-amd64.deb
gdebi --n shiny-server-1.5.16.958-amd64.deb
rm shiny-server-1.5.16.958-amd64.deb
