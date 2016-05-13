FROM python:3

MAINTAINER mattjmcnaughton@gmail.com

# Add the code to `/sdep` and use as a dep.
ADD . /sdep
WORKDIR /sdep

# Update pip and download the development dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
