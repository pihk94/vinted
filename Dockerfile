# VERSION 0.0.1
# AUTHOR: Melchior PRUGNIAUD
# DESCRIPTION: Discord vinted container for production use


FROM python:3.9.7-slim-buster
LABEL maintainer="Melchior PRUGNIAUD"
ENV DISCORD_TOKEN=""

COPY . .

RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -U pip setuptools==58.0.1 wheel \
    && pip install --no-cache-dir -e .

CMD ["python", "vinted/app.py"]