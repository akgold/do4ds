# syntax=docker/dockerfile:1
FROM rstudio/plumber
MAINTAINER alexkgold@gmail.com

COPY renv.lock .
COPY . /api/

RUN R -e "install.packages('renv', repos = 'https://packagemanager.rstudio.com/all/__linux__/focal/latest')"
RUN R -e "renv::restore()"

CMD ["/api/plumber.R"]
