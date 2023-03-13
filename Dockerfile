FROM ubuntu:22.04
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install pygeohash mariadb requests netaddr

ADD init.sql /config/initdb.d/

ADD . /app


CMD ["python", "app.py"]