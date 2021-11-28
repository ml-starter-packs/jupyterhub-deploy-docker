#!/bin/sh
apt-get update && \
	apt-get upgrade -yq && \
	apt-get install -y \
	curl \
	htop \
	fzf \
	less \
	openssh-client \
	ripgrep \
	screen \
	vim \
	jq \
	&& \
	apt-get -qq purge && \
	apt-get -qq clean && \
	rm -rf /var/lib/apt/lists/*
