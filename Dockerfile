FROM ubuntu:precise

MAINTAINER Tim Akinbo <takinbo@timbaobjects.com>

RUN apt-get update

RUN apt-get install -y python-dev build-essential python-setuptools git-core file libxml2-dev libxslt1-dev vim
RUN easy_install pip
RUN pip install -U setuptools

ADD requirements.txt /app/
RUN pip install --find-links=https://pypi.timbaobjects.com/ndi/apollo/wheels/ -r /app/requirements.txt

ADD README /app/
ADD apollo/ /app/apollo/
ADD doc/ /app/doc/
ADD Procfile.docker /app/Procfile
ADD manage.py /app/

RUN pybabel compile -d /app/apollo/frontend/translations/

WORKDIR /app/
CMD ["honcho","start"]
EXPOSE 5000
