import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class EchoHandler(BaseHTTPRequestHandler):
    # Отключаем вывод логов каждого запроса в консоль (по желанию)
    def log_message(self, format, *args):
        return

    def _collect_request_data(self):
        # 1. Метод (GET, POST, PUT, DELETE...)
        method = self.command
        
        # 2. Путь и параметры (например, /api/test?user=1)
        path = self.path

        # 3. Заголовки. dict(self.headers) преобразует объект заголовков в обычный словарь
        headers = dict(self.headers)

        # 4. Тело запроса
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b""
        
        # Попытаемся декодировать тело как JSON, если это возможно
        body_text = raw_body.decode('utf-8', errors='replace')
        json_body = None
        if content_length > 0 and 'application/json' in headers.get('Content-Type', ''):
            try:
                json_body = json.loads(body_text)
            except json.JSONDecodeError:
                pass # Если это не валидный JSON, оставим json_body пустым

        return {
            "method": method,
            "path": path,
            "headers": headers,
            "content_length": content_length,
            "body_raw": body_text,
            "body_json": json_body
        }

    def _send_json_response(self, data, status=200):
        """Вспомогательный метод для отправки JSON"""
        response_body = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        # Полезный заголовок для CORS, чтобы запросы шли из браузера
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.end_headers()
        
        self.wfile.write(response_body)

    def do_GET(self):
        data = self._collect_request_data()
        self._send_json_response(data)

    def do_POST(self):
        data = self._collect_request_data()
        self._send_json_response(data)

    def do_PUT(self):
        data = self._collect_request_data()
        self._send_json_response(data)

    def do_DELETE(self):
        data = self._collect_request_data()
        self._send_json_response(data)

    def do_PATCH(self):
        data = self._collect_request_data()
        self._send_json_response(data)

if __name__ == "__main__":
    # ThreadingHTTPServer позволяет обрабатывать несколько запросов одновременно
    server = ThreadingHTTPServer(('0.0.0.0', int(os.getenv('PORT', 8000))), EchoHandler)
    print("Сервер запущен на http://0.0.0.0:8000")
    print("Нажмите Ctrl+C для остановки.")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    server.server_close()
    print("Сервер остановлен.")