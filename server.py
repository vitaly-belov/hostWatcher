import sqlite3
import http.server
import socketserver
import sys

PORT = 8000

def get_activities():
    con = sqlite3.connect("host_watcher.db")
    cur = con.cursor()
    cur.execute("SELECT ping_time, address, mac FROM activity")
    activities = cur.fetchall()
    con.close()
    return activities

if __name__ == "__main__":
        print(get_activities())
        for record in get_activities():
            print(f'{record[0]},{record[1]},{record[2]}')
   
    # Handler = http.server.SimpleHTTPRequestHandler
    # with socketserver.TCPServer(("", PORT), Handler) as httpd:
    #     print("serving at port", PORT)
    #     httpd.serve_forever()

