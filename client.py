import socket
import time
import sched


def send_udp_packet(scheduler, interval, i):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    addr = ("192.168.1.11", 12001)

    now = int(time.time() * 1000000)
    t_bytes = now.to_bytes(511, 'little')
    t_bytes += int.to_bytes(i, 1)
    i = (i + 1) % 256

    client_socket.sendto(t_bytes, addr)
    scheduler.enter(interval, 1, send_udp_packet, (scheduler, interval, i))


scheduler = sched.scheduler(time.time, time.sleep)
interval = 0.008  # 8 milliseconds
i = 0

scheduler.enter(0, 1, send_udp_packet, (scheduler, interval, i))
scheduler.run()
