ARG DOCKER_NOTEBOOK_IMAGE
FROM $DOCKER_NOTEBOOK_IMAGE
ARG JUPYTERHUB_VERSION

USER root
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	dvipng \
	fonts-lato \
	fonts-dejavu \
	gcc \
	gfortran \
	ghostscript \
	imagemagick \
	lmodern \ 
	&& \
	apt-get -qq purge && \
	apt-get -qq clean && \
	rm -rf /var/lib/apt/lists/*


# Dev tools
USER root
COPY install_dev_tools.sh /tmp/
RUN /tmp/install_dev_tools.sh

# Final cleaning and user customizations
USER $NB_UID
RUN \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER root
COPY install_vscode.sh /tmp/
RUN /tmp/install_vscode.sh

USER $NB_UID
# RUN mamba install xeus-python -y
RUN pip install jupyter_server_proxy jupyterlab-miami-nights
RUN pip install black flake8 autopep8 isort pre-commit

COPY install_jupyter_nbextensions.sh /tmp/
# RUN /tmp/install_jupyter_nbextensions.sh

COPY install_language_server.sh /tmp/
RUN /tmp/install_language_server.sh

COPY install_monitoring.sh /tmp/
# RUN /tmp/install_monitoring.sh
COPY install_hugo.sh /tmp/
COPY install_geckodriver.sh /tmp/

USER root
## CONFIG
# Copy over config which creates launcher icons in jupyterlab
COPY jupyter_notebook_config.py /home/jovyan/.jupyter/
RUN mkdir -p /home/$NB_USER/.jupyter/lab/workspaces/
COPY ./jupyterlab_settings /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab
RUN chmod -R 777 /home/$NB_USER/.jupyter/lab

USER $NB_UID

# USER SETTINGS
RUN echo "export EDITOR=/usr/bin/vim" >> /home/$NB_USER/.bashrc
RUN echo "export PAGER=less" >> /home/$NB_USER/.bashrc

# remember git login credentials
RUN git config --global credential.helper "cache --timeout 144000"
