FROM python:2.7.13
MAINTAINER Marsel Mavletkulov <marselester@ya.ru>

CMD ["uwsgi"]
EXPOSE 8000
WORKDIR /olympus-app/

ENV PIP_NO_CACHE_DIR="off" \
    UWSGI_CHDIR="/olympus-app" \
    UWSGI_MODULE="olympus.wsgi" \
    UWSGI_SOCKET="0.0.0.0:8000" \
    UWSGI_HTTP="0.0.0.0:80" \
    UWSGI_PROCESSES="4" \
    UWSGI_MASTER="true" \
    UWSGI_NO_ORPHANS="true" \
    UWSGI_VACUUM="true" \
    UWSGI_DIE_ON_TERM="true" \
    UWSGI_HARAKIRI_VERBOSE="true"

COPY ./requirements.txt /olympus-app/

RUN pip install uwsgi==2.0.15 && \
    pip install -r /olympus-app/requirements.txt

COPY ./olympus/ /olympus-app/olympus/
