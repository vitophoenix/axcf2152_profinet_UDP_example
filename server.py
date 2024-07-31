import socket
from time import strftime, localtime
import csv

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))
last_timestamp_receiver = 0
last_timestamp_tx = 0
intervals = []

with open('profinet_dump.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    while True:
        message, address = server_socket.recvfrom(1024)
        # extract timestamp
        # if len(message) != 0:
        timestamp_receiver = int.from_bytes(message[0:8], "little")
        delta_receiver = timestamp_receiver - last_timestamp_receiver
        # print("cycle: " + str(timestamp) + 'us, timestamp: ' + str(delta/1000) + 'ms')
        last_timestamp_receiver = timestamp_receiver

        timestamp_tx = int.from_bytes(message[8:16], "little")
        delta_tx = timestamp_tx - last_timestamp_tx
        # print("cycle: " + str(timestamp) + 'us, timestamp: ' + str(delta/1000) + 'ms')
        last_timestamp_tx = timestamp_tx
        intervals.append((timestamp_receiver, delta_receiver/1000, timestamp_tx, delta_tx/1000, delta_tx == 0))
        if len(intervals) >= 100:
            print('printing 100 intervals...')
            for values in intervals:
                # print(str(values) + ' '+ strftime('%Y-%m-%d %H:%M:%S', localtime(values[0]/1000000)))
                print(str(values))
                writer.writerow(values)
            intervals = []
