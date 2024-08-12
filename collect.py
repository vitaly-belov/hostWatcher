import threading
from icmplib import ping
from getmac import get_mac_address
import sqlite3
import time

prefix = '192.168.0.'
result = [None] * 254

def pingHost(host):
    address = prefix + str(host)
    hostObject = ping(address, count=1, interval=1, timeout=2, id=None, source=None, family=None, privileged=True)
    if hostObject.is_alive:
        lock = threading.RLock()
        with lock:
            result[host-1] = (address)



if __name__ == "__main__":
    hosts = (i for i in range(1, 255))
    for host in hosts:
        thread = threading.Thread(target=pingHost, args=(host,))
        thread.start()

con = sqlite3.connect("host_watcher.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS activity(ping_time, address, mac)")

rows = []

for i in range(1,255):
    if result[i - 1]:
        address = '192.168.8.' + str(i)
        mac = get_mac_address(ip=address)
        now = time.time()
        row = tuple([str(now), str(address), str(mac)])
        rows.append(row)


print(rows)
sql = 'INSERT INTO activity VALUES (?, ?, ?)'
cur.executemany(sql, rows)
con.commit()
con.close()