#FROM python:3.8
FROM osgeo/gdal

RUN apt-get update && apt-get install --yes python3-pip \
                        python3-gdal 

                        # gdal-bin \
                        # libgdal-dev \
                        # gettext \
                        # python3-gdal


# RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
# RUN export C_INCLUDE_PATH=/usr/include/gdal

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000
