FROM course-e8e9:241250086
USER root
RUN apt-get -o Acquire::Retries=1 -o Acquire::https::Timeout=20 update && apt-get install -y --no-install-recommends strace && rm -rf /var/lib/apt/lists/*
COPY services/buildchecker /app/
ENV PYTHONPATH=/app
WORKDIR /course
