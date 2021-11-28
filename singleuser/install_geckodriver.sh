#!/bin/sh
HUGO_VER=0.53
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
	tar -xvzf geckodriver* && \
	chmod +x geckodriver && \
	mv geckodriver /usr/sbin/ && \
	rm geckodriver*
