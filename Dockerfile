FROM nikolaik/python-nodejs:python3.6-nodejs14

COPY . pa/

WORKDIR pa/

RUN make install-client-deps
RUN make build-client
RUN make install-server-deps

ENTRYPOINT ["make", "run-server-prod"]
