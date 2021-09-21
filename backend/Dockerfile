FROM osgeo/gdal:ubuntu-small-3.3.2

RUN apt-get update && apt-get install --yes python3-pip \
                        python3-gdal \
                        gettext

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000
