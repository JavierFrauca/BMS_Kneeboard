import threading
from httpserver import iniciar_servidor_web
from checkfiles import verificar_cambios
import config

# Cargamos configuracion
config.cargar_variables()
# Mostar configuracion
print("Escaneando carpeta " + config.ruta_bms)

# Hilo para verificar cambios en el fichero
hilo_verificar_cambios = threading.Thread(target=verificar_cambios)
hilo_verificar_cambios.daemon = True
hilo_verificar_cambios.start()

# Hilo para iniciar el servidor web
hilo_servidor_web = threading.Thread(target=iniciar_servidor_web)
hilo_servidor_web.daemon = True
hilo_servidor_web.start()

# Mantén el programa principal en ejecución
while True:
    pass
