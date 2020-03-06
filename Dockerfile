FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install nano wget

RUN mkdir Repos
RUN mkdir Repos/debian-output

WORKDIR Repos/debian-output
RUN wget https://mssqlcli.blob.core.windows.net/daily/deb/mssql-cli-dev-latest.deb
