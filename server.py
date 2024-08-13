import sqlite3
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

PORT = 8000

def get_activities():
    con = sqlite3.connect("host_watcher.db")
    cur = con.cursor()
    sql = '''
        SELECT t.ping_time, t.address, t.mac, t.prefix, t.host
        FROM activity t
        INNER JOIN (
            SELECT address, max(ping_time) as max_ping_time
            FROM activity
            GROUP BY address
        ) tm ON t.address = tm.address and t.ping_time = tm.max_ping_time
        ORDER BY t.prefix, t.host
    '''
    cur.execute(sql)
    activities = cur.fetchall()
    con.close()
    return activities


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>HostWatcher</title></head>'.encode())
        self.wfile.write('<body>'.encode())
        self.wfile.write('<table>'.encode())
        self.wfile.write('<tr>'.encode())
        self.wfile.write('<th>Time</th>'.encode())
        self.wfile.write('<th>IP</th>'.encode())
        self.wfile.write('<th>MAC</th>'.encode())
        self.wfile.write('</tr>'.encode())
        for record in get_activities():
            self.wfile.write('<tr>'.encode())
            self.wfile.write(f'<td style="border: 1px solid lightgray;  border-radius: 10px; padding: 6px;">{record[0]}</td>'.encode())
            self.wfile.write(f'<td style="border: 1px solid lightgray;  border-radius: 10px; padding: 6px;">{record[1]}</td>'.encode())
            self.wfile.write(f'<td style="border: 1px solid lightgray;  border-radius: 10px; padding: 6px;">{record[2]}</td>'.encode())
            self.wfile.write('<tr>'.encode())

        self.wfile.write('</table>'.encode())
        self.wfile.write('</body></html>'.encode())

def main():
        print(get_activities())
        run(handler_class=HttpGetHandler)


if __name__ == "__main__":
   main()

