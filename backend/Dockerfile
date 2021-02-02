FROM python:3.8

RUN apt-get update && apt-get install --yes proj-bin \
                        libgdal-dev

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN gdal-config --version
RUN pip install -r requirements.txt
EXPOSE 8000

