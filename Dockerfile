FROM python:3.6-slim-buster

RUN apt-get update -yy && \
    apt-get install -yy make python3.6 python3-pip

COPY . pa/

WORKDIR pa/

RUN make init

ENTRYPOINT ["./entrypoint.sh"]
