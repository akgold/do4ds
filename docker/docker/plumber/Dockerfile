# syntax=docker/dockerfile:1
FROM rstudio/plumber
MAINTAINER alexkgold@gmail.com

COPY renv.lock .

RUN R -e "install.packages('renv', repos = 'https://packagemanager.rstudio.com/all/__linux__/focal/latest')"
RUN R -e "renv::restore()"

# Copy project files -- might change frequently so do late
COPY . /api/
CMD ["/api/plumber.R"]
