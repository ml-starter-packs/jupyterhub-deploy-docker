#!/bin/sh
# Installs language server and creates symlinks to enable discovery of code sources
pip install 'jupyterlab~=3.0.0' && \
	pip install jupyterlab-lsp==3.9.1 jupyter-lsp==1.5.0 && \
	pip install git+https://github.com/krassowski/python-language-server.git@main && \
	#pip install 'python-lsp-server[all]' && \
	mkdir -p ~/.lsp_symlink && \
	cd ~/.lsp_symlink && \
	ln -s /home home && \
	ln -s /opt opt && \
	# pip install \
	# pydocstyle \
	# pyflakes \
	# pylint \
	# rope \
	# yapf \
	# mccabe \
	# && \
	mkdir -p ~/.config && \
	echo "[pycodestyle]" > ~/.config/pycodestyle && \
	echo "ignore = E402, E703, W391" >> ~/.config/pycodestyle && \
	echo "max-line-length = 88" >> ~/.config/pycodestyle && \
	echo "finished installing language server"
