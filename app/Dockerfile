FROM python:3.8-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH /usr/local/lib

# install psycopg2 dependencies
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

RUN apk add --update --no-cache \ 
    freetype-dev jpeg-dev zlib-dev libjpeg libffi-dev


# Install postgres client
RUN apk add --update --no-cache postgresql-client

# install dependencies
RUN pip install --upgrade pip
WORKDIR /usr/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/app
COPY . .

# RUN python manage.py runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
