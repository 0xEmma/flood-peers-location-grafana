from netaddr import *
import requests
import json
import socket, struct
import time
import pygeohash
import IP2Location, os
# import mariadb

#To convert the IP address in xxx.xxx.xxx.xxx to a decimal number
def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


#qbittorrent credentials
server_ip = os.environ['flood_server']
server_address = "http://" + server_ip

s = requests.Session()

json_data = {
    'username': os.environ['flood_username'],
    'password': os.environ['flood_password'],
}

response = s.post(f'{server_address}/api/auth/authenticate', json=json_data)
torrents = json.loads(s.get(server_address + "/api/torrents").text)
torrents = torrents['torrents']

# #Logging into mariadb server / Enter your mariadb credentials here
mydb = mariadb.connect(
          host="mariadb-svc.default.svc.cluster.local",
          port=3306,
          user="ip2location",
          password="123456",
          database="ip2location",
          autocommit=True
)

current_time = str(int(time.time()))

for torrent in torrents:
    torrent_peers = json.loads(s.get(server_address + "/api/torrents/" + torrent + "/peers").text)

    #Get IP address of every peer of every torrent
    for peer in torrent_peers:
        print(peer)
        ip = peer['address']
        print(ip)
        # mycursor = mydb.cursor()
        database = IP2Location.IP2Location(os.path.join("IP2LOCATION-LITE-DB5.BIN"))
        record = database.get_all(ip)
        print(record.latitude)
        print(record.longitude)
        geohash = pygeohash.encode(float(record.latitude), float(record.longitude))
        if record.latitude == 0 and record.longitude == 0:
            continue #Sometimes (especially in public trackers) some IP's in the private IP space show up as peers. This should filter those.
        mycursor = mydb.cursor()
        query = "INSERT INTO ip2location.peer_list(time, ip_address, geohash) VALUES (" + current_time + ",'" + str(ip) + "','" + geohash + "');"
        mycursor.execute(query)




# s.get(server_address + "/api/v2/auth/logout")

