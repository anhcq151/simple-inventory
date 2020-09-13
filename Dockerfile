FROM python:3.8-slim-buster

ARG username=inventory
ARG user_uid=1000
ARG user_gid=${user_uid}
ARG workdir=/opt/simple-inventory
ARG data=${workdir}/data
ENV DATABASE_URL=sqlite:///${data}/inventory.db
WORKDIR ${workdir}
RUN groupadd --gid ${user_gid} ${username} \
    && useradd -s /bin/bash --uid ${user_uid} --gid ${user_gid} ${username} \
    && pip3 install gunicorn flask flask-migrate flask-wtf flask-sqlalchemy --disable-pip-version-check --no-cache-dir

COPY new ${workdir}/new
RUN mkdir -p ${data} && chown -R ${username}:${username} ${workdir}

USER ${username}
EXPOSE 5000

ENTRYPOINT [ "gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "new:newapp" ]