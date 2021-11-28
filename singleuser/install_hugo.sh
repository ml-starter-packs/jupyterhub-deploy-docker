#!/bin/sh
HUGO_VER=0.53
wget https://github.com/gohugoio/hugo/releases/download/v${HUGO_VER}/hugo_${HUGO_VER}_Linux-64bit.deb && \
	dpkg -i hugo*.deb && \
	rm hugo*.deb
