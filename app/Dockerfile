FROM python:3.8-alpine

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

RUN apk add --update --no-cache \
    xvfb libgcc libstdc++ libx11 glib libxrender libxext libintl \
    ttf-dejavu ttf-droid ttf-freefont ttf-liberation 

# On alpine static compiled patched qt headless wkhtmltopdf (46.8 MB).
# Compilation took place in Travis CI with auto push to Docker Hub see
# BUILD_LOG env. Checksum is printed in line 13685.
COPY --from=madnight/alpine-wkhtmltopdf-builder:0.12.5-alpine3.10-606718795 \
    /bin/wkhtmltopdf /bin/wkhtmltopdf

RUN ln -s /bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf;
RUN chmod +x /usr/local/bin/wkhtmltopdf;

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
