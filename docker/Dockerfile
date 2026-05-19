FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && mkdir -p /app \
    && chgrp -R 0 /app \
    && chmod -R g=u /app

COPY flaskAlert.py /app/flaskAlert.py
COPY docker/run.sh /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 9119

ENTRYPOINT ["/app/run.sh"]
