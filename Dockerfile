FROM python:3

MAINTAINER mattjmcnaughton@gmail.com

# Add the code to `/sdep` and use as a dep.
ADD . /sdep
WORKDIR /sdep

# Update pip, download the development dependencies, and download the `sdep`
# dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python setup.py develop
