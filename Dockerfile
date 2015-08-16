FROM ubuntu:latest

# ENV LAST_UPDATED 12/05/14 v2

# output python
ENV PYTHONUNBUFFERED 1

# update requirements
RUN apt-get update

# install the base required packages
RUN apt-get install -y python-dev libjpeg-dev libpq-dev

# install deployment specific tools
RUN apt-get install -y nginx
RUN apt-get install -y supervisor

# install pip
RUN apt-get install -y python-pip

ADD src/requirements /home/docker/code/src/requirements
ADD etc /home/docker/code/etc

# create sockets for nginx and uwsgi
RUN touch /home/docker/code/app.sock && chown www-data /home/docker/code/app.sock

# install requirements
RUN pip install -r /home/docker/code/src/requirements/production.txt

# setup nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /home/docker/code/etc/nginx.conf /etc/nginx/sites-enabled/
RUN ln -s /home/docker/code/etc/supervisor.conf /etc/supervisor/conf.d/

EXPOSE 80