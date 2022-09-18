apt-get -yqq update
apt-get -yqq install gnupg2 ca-certificates

# add CRAN to apt sources
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
printf '\n#CRAN mirror\ndeb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/\n' | tee -a /etc/apt/sources.list

# update apt
apt-get -y update
apt-get -y upgrade

# requisites for RStudio
apt-get -y install gdebi-core

# requisites for different R packages
# this aims at covering as much packages as possible
# see https://packagemanager.rstudio.com/client/#/repos/1/overview
# and also
# https://geocompr.github.io/post/2020/installing-r-spatial-ubuntu/
# http://dirk.eddelbuettel.com/blog/2020/06/22#027_ubuntu_binaries
# this a broad, general setup, no fine detail here
apt-get -y install software-properties-common libopenblas-dev libsodium-dev texlive default-jdk

# saw error about this
apt-get -y install libharfbuzz-dev libfribidi-dev

add-apt-repository -y ppa:c2d4u.team/c2d4u4.0+
apt-get -y update

# install R
apt-get -y install r-base r-base-dev
R CMD javareconf

# SPM site-wide
sed -i 's/cloud\.r-project\.org/packagemanager\.rstudio\.com\/all\/latest/g' /usr/lib/R/etc/Rprofile.site

