FROM ubuntu:22.04
RUN apt update
RUN apt install -y python3 python3-pip
RUN apt-get install -y libmariadb-dev
RUN pip3 install pygeohash mariadb requests netaddr

ADD init.sql /config/initdb.d/

ADD . /app
WORKDIR /app

CMD ["python", "/app/qbittorrent_peers_location_grafana.py"]
