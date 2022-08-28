#!/usr/bin/sh
apt-get -y update

# install R packages
apt-get -y install r-cran-devtools r-cran-usethis r-cran-tidyverse r-cran-janitor r-cran-writexl r-cran-data.table r-cran-roxygen2 r-cran-knitr r-cran-rmarkdown r-cran-bookdown r-cran-xaringan r-cran-rdpack r-cran-dbi r-cran-dbplyr r-cran-rmariadb r-cran-rpostgres r-cran-glue r-cran-doparallel r-cran-future r-cran-shiny r-cran-shinyjs r-cran-shinydashboard r-cran-dt

R --vanilla << EOF
options(repos = c(REPO_NAME = "https://packagemanager.rstudio.com/all/latest"))
install.packages("tidymodels")
install.packages("pkgdown")
install.packages("highcharter")
q()
EOF

apt-get -qq purge
apt-get -qq clean
rm -rf /var/lib/apt/lists/*
