# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# Copy external files
RUN mkdir -p /project/
RUN mkdir -p /project/out/

COPY ./requirements.txt /project/
COPY ./hello.ipynb /project/
COPY ./_quarto.yml /project/

# Install system packages
RUN apt-get update && apt-get install -y \
  wget python3 python3-pip

# Install quarto CLI + clean up
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v0.9.83/quarto-0.9.83-linux-amd64.deb
RUN dpkg -i ./quarto-0.9.83-linux-amd64.deb
RUN rm -f ./quarto-0.9.83-linux-amd64.deb

# Install Python requirements
RUN pip3 install -r /project/requirements.txt

# Render notebook
CMD cd /project && \
  quarto render ./hello.ipynb

