# pull official base image
FROM python:3.6.8-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies requirements
RUN apt-get update
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install libsm6 libxrender-dev libxext6

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

#