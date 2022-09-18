FROM docker.io/ubuntu:focal-20210921

ENV DEBIAN_FRONTEND=noninteractive

COPY install_r_deps.sh /tmp/
RUN /tmp/install_r_deps.sh

COPY install_r.sh /tmp/
RUN /tmp/install_r.sh

# SPM site-wide (???)
RUN sed -i 's/cloud\.r-project\.org/packagemanager\.rstudio\.com\/all\/latest/g' /usr/lib/R/etc/Rprofile.site

# original reference: https://github.com/pachadotdev/rstudio-server-droplet
COPY install_rstudio.sh /tmp/
RUN /tmp/install_rstudio.sh

COPY install_rshiny.sh /tmp/
RUN /tmp/install_rshiny.sh

COPY install_r_pkgs.sh /tmp/
RUN /tmp/install_r_pkgs.sh

CMD rstudio-server start && shiny-server
