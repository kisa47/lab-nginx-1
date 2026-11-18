from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        server_name = os.getenv('SERVERNAME', 'SERVERNAME')

        self.wfile.write(server_name.encode('utf-8'))

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    server_address = ('', int(os.getenv('PORT', 8000)))
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Сервер запущен на порту 8000. Нажмите Ctrl+C для остановки.")
    try:
        # Запускаем бесконечный цикл обработки входящих соединений
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Сервер остановлен.")