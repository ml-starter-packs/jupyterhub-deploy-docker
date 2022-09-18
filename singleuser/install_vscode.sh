#!/bin/sh
apt-get update && \
	apt-get install -y --no-install-recommends \
	curl && \
	echo "getting latest install script" && \
	curl -fsSL https://code-server.dev/install.sh > install.sh && \
	sh install.sh --version 4.5.2 && \
	rm install.sh && \
	apt-get -qq purge curl && \
	apt-get -qq purge && \
	apt-get -qq clean && \
	rm -rf /var/lib/apt/lists/*

