FROM m.daocloud.io/docker.io/library/python:3.13-slim@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74
WORKDIR /work
COPY src ./src
COPY include ./include
COPY Makefile ./
RUN sed -i "s/deb.debian.org/mirrors.huaweicloud.com/g" /etc/apt/sources.list.d/debian.sources && apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN make
CMD ["./minicalc", "1+2*3"]
