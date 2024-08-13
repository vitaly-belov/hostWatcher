import sqlite3
import http.server
import socketserver
import sys

PORT = 8000

def get_activities():
    con = sqlite3.connect("host_watcher.db")
    cur = con.cursor()
    sql = '''
        SELECT t.ping_time, t.address, t.mac
        FROM activity t
        INNER JOIN (
            SELECT address, max(ping_time) as max_ping_time
            FROM activity
            GROUP BY address
        ) tm ON t.address = tm.address and t.ping_time = tm.max_ping_time
    '''
    cur.execute(sql)
    activities = cur.fetchall()
    con.close()
    return activities


def http():
     pass
    # Handler = http.server.SimpleHTTPRequestHandler
    # with socketserver.TCPServer(("", PORT), Handler) as httpd:
    #     print("serving at port", PORT)
    #     httpd.serve_forever()


def main():
        print(get_activities())
        for record in get_activities():
            print(f'{record[0]},{record[1]},{record[2]}')



if __name__ == "__main__":
   main()

