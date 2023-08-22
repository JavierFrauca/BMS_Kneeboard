import config
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
# Clase para manejar las solicitudes del servidor web
class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        fichero_html = os.path.splitext(config.fichero_con_ruta)[0] + '.html'
        if os.path.exists(fichero_html):
            self._set_response()
            # Abre y envía el fichero HTML procesado
            with open(fichero_html, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self._set_response()
            mensaje = "<h1>Briefing no disponible</h1>"
            self.wfile.write(mensaje.encode())
# Función para iniciar el servidor web en un hilo separado
def iniciar_servidor_web():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Servidor web iniciado en el puerto 8080...")
    httpd.serve_forever()