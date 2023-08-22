import os
import pickle

#variables globales
ruta_bms = ""
fichero_briefing = ''
fichero_con_ruta = ''

def cargar_variables():
    global ruta_bms, fichero_briefing, fichero_con_ruta
    # Intenta cargar el valor de la variable desde un archivo existente
    try:
        with open('config.pkl', 'rb') as archivo:
            print("Recuperando valores")      
            datos = pickle.load(archivo)
            ruta_bms = datos['ruta_bms']
            fichero_briefing = datos['fichero_briefing']
            fichero_con_ruta = os.path.join(ruta_bms, fichero_briefing)
        if ruta_bms is None or fichero_briefing is None:
            grabar_variables()
    except FileNotFoundError:
        print("No se encontró el archivo 'config.pkl'. Se le preguntará por las variables")
        grabar_variables()
def grabar_variables():
    global ruta_bms, fichero_briefing, fichero_con_ruta
    print("Valores de configuracion")      
    ruta_bms = input("Ruta de bms: ")
    fichero_briefing = input("Nombre fichero briefing: ")
    fichero_con_ruta = os.path.join(ruta_bms, fichero_briefing)
    datos = {
        'ruta_bms': ruta_bms,
        'fichero_briefing': fichero_briefing
    }
    with open('config.pkl', 'wb') as archivo:
        pickle.dump(datos, archivo)  
        print("Se ha guardado la configuración")      