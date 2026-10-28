FROM docker.io/library/python@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74
WORKDIR /work
COPY main.c Makefile ./
RUN sed -i "s@http://deb.debian.org@https://deb.debian.org@g;s@https://deb.debian.org@https://deb.debian.org@g" /etc/apt/sources.list.d/debian.sources \
    && apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=60 -o Acquire::https::Timeout=60 update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN make
CMD ["echo", "hello E3"]
