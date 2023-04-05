FROM osgeo/gdal:ubuntu-small-3.3.1

RUN apt update \
&& apt-get install -y cron \
&& apt-get install -y fuseiso \
&& apt-get install -y nano \
&& apt update \
&& apt-get install python3-pip -y --fix-missing

COPY ./requirements.txt /wikibet/requirements.txt
RUN pip3 install -r /wikibet/requirements.txt

RUN pip3 install gunicorn

COPY ./ /wikibet 
COPY ./start.sh /wikibet/start.sh
RUN mkdir -p /vfs

WORKDIR /wikibet
USER root
RUN chmod +x /wikibet/start.sh

EXPOSE 7777
ENTRYPOINT ["/wikibet/start.sh"]

# docker build -t hub.jool-tech.com/library/client-server-pp:3.1 .
# docker run hub.jool-tech.com/library/client-server-pp:2.8 .
# docker push hub.jool-tech.com/library/client-server-pp:3.1 
