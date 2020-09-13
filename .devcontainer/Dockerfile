FROM python:3.8-slim-buster

ARG workdir=/opt/simple-inventory
ARG data=${workdir}/data
ENV DATABASE_URL=sqlite:///${data}/inventory.db
WORKDIR ${workdir}
RUN pip3 install python-dotenv flask flask-migrate flask-wtf flask-sqlalchemy pylint autopep8 --disable-pip-version-check --no-cache-dir \
    && apt update \
    && apt install -y git

EXPOSE 5000
