FROM m.daocloud.io/docker.io/library/python:3.13-slim@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74
WORKDIR /work
COPY main.c helper.c config.h extra.h unused.h Makefile ./
RUN make app
CMD ["./app"]
