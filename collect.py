import threading
from icmplib import ping
from getmac import get_mac_address
import sqlite3
from datetime import datetime
import sys

prefix = ''
result = [None] * 254

def pingHost(host):
    global prefix
    address = prefix + '.' + str(host)
    hostObject = ping(address, count=1, interval=1, timeout=2, id=None, source=None, family=None, privileged=True)
    if hostObject.is_alive:
        lock = threading.RLock()
        with lock:
            global result
            result[host-1] = (address)

def main():
    args = sys.argv[1:]
    global prefix
    prefix = args[0]
    
    hosts = (i for i in range(1, 255))
    for host in hosts:
        thread = threading.Thread(target=pingHost, args=(host,))
        thread.start()

    con = sqlite3.connect("host_watcher.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS activity(ping_time, address, mac, prefix, host)")

    rows = []

    for i in range(1,255):
        if result[i - 1]:
            address = prefix + '.' + str(i)
            mac = get_mac_address(ip=address)
            now = datetime.now()
            fmt_now = now.strftime("%Y-%m-%d %H:%M:%S")
            row = tuple([fmt_now, str(address), str(mac), prefix, i])
            rows.append(row)


    print(rows)
    sql = 'INSERT INTO activity VALUES (?, ?, ?, ?, ?)'
    cur.executemany(sql, rows)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()