FROM python:3.8-alpine
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH /usr/local/lib

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev alpine-sdk gdal-dev
RUN apk update && apk upgrade \
    && apk add postgresql-client \
        postgresql-dev \
        musl-dev \
        gcc \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        gettext-dev \
    && apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        libcrypto1.1 \
    && apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        gdal-dev \
        geos-dev

# Install postgres client
RUN apk add --update --no-cache postgresql-client

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "check_db_connection.py"]
# RUN python check_db_connection.py
