FROM python:3.6

COPY . pa/

WORKDIR pa/

RUN make install-server-deps

ENTRYPOINT ["make", "run-server-prod"]
