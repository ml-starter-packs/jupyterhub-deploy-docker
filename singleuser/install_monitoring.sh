#!/bin/sh
python3 -m pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION nbresuse && \
	jupyter labextension install --minimize=False jupyterlab-topbar-extension && \
	jupyter labextension install --minimize=False jupyterlab-system-monitor && \
	npm cache clean --force && \
	rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
	rm -rf /home/$NB_USER/.cache/yarn && \
	rm -rf /home/$NB_USER/.node-gyp && \
	fix-permissions $CONDA_DIR && \
	fix-permissions /home/$NB_USER
