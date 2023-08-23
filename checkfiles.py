import config
import os
import hashlib
import time

# Hash del fichero inicial
hash_inicial = None
def detect_encoding(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return 'UTF-8'
    except UnicodeDecodeError:
        return 'ANSI'
# Función para procesar el fichero y convertirlo en HTML
def procesar_fichero(ruta_fichero):
    # Variable para almacenar las líneas del archivo
    contenido = ''
    indice = ''
    group_pos = -1
    group_name = ''
    line = 0
    in_table = False
    # Lee los bytes del fichero
    with open(ruta_fichero, 'rb') as file:
        contenido_bytes = file.read()
        # Decodifica los bytes a texto utilizando UTF-8
        if detect_encoding(ruta_fichero) == 'UTF-8':
            contenido_texto = contenido_bytes.decode('utf-8')
        else:
            contenido_texto = contenido_bytes.decode('ansi')
        for linea in contenido_texto.splitlines():
            # Agregar la línea al contenido
            if len(linea.strip()) == 0:
                pass
                #if len(contenido) > 0: contenido += "</table>" + "\n"
                #contenido += "<table>" + "\n"
            elif linea.startswith("--------"):
                pass
            elif linea.startswith("\t"):
                linea_bruta = linea
                linea = linea.strip()  # Eliminar espacios en blanco al principio y al final de la línea
                #le damos formato de tabla
                if group_name.startswith('Mission Overvi'):
                    if line == 0:
                        contenido +=  '<h2>'+ linea + r'</h2>' + '\n'
                        contenido += "<table>" + "\n"
                        in_table = True
                    else:
                        contenido += "<tr><td>" + linea.replace("\t", "</td><td>") + "</td></tr>" + '\n'
                elif group_name.startswith('Situation:'):
                    if line < 2:
                        #es raro este bloque, tiene un texto que interfiere con la tabla posterior
                        contenido +=  '<p>'+linea + r'</p>' + '\n'
                    elif line==2:
                        contenido += "<table>" + "\n"
                        in_table = True
                        contenido += "<tr><td>" + linea.replace("\t", "</td><td>") + "</td></tr>" + '\n'
                        #contenido += "<tr><th>" + linea.replace("\t", "</th><th>") + "</th></tr>" + '\n'
                    else:
                        contenido += "<tr><td>" + linea.replace("\t", "</td><td>") + "</td></tr>" + '\n'
                elif group_name.startswith('Ordnance:'):
                    if line==0:
                        contenido += "<table>" + "\n"
                        in_table = True
                        contenido += "<tr><th>" + linea.replace("\t", "</th><th>") + "</th></tr>" + '\n'
                    elif linea_bruta.startswith("\t \t"):
                        contenido += "<tr><td>" + linea[2:].replace("\t", "</td><td>") + "</td></tr>" + '\n'
                    else:
                        contenido += "<tr><td></td><td>" + linea.replace("\t", "</td><td>") + "</td></tr>" + '\n'
                elif group_name.startswith('Support:'):
                    contenido +=  '<p>'+linea + r'</p>' + '\n'
                elif group_name.startswith('Rules of Engage'):
                    contenido +=  '<p>'+linea + r'</p>' + '\n'
                elif group_name.startswith('Emergency Proce'):
                    contenido +=  '<p>'+linea + r'</p>' + '\n'
                else:
                    if line==0:
                        contenido += "<table>" + "\n"
                        in_table = True
                        contenido += "<tr><th>" + linea.replace("\t", "</th><th>") + "</th></tr>" + '\n'
                    else:
                        contenido += "<tr><td>" + linea.replace("\t", "</td><td>") + "</td></tr>" + '\n'
                line += 1
            elif linea.startswith('BRIEFING RECORD '):
                #es la cabecera, metelo como h2 suficiente
                contenido += '<hr><h2>' + linea + '</h2><hr>' + '\n'
            elif linea.startswith('END_OF_BRIEFING'):
                #es la cabecera, metelo como h2 suficiente
                contenido += '</table>'
                contenido += '<hr><h2>' + linea + '</h2><hr>' + '\n'
            else:
                line = 0
                group_name = linea
                group_pos+=1
                group_id = linea[:15].replace(" ","_").replace(":","")
                if in_table == True: contenido+="</table>" + '\n'
                contenido += '<h1 id="'+group_id+'">' + group_name + '</h1>' + '\n'
                indice += '<div style="overflow:hidden;position:relative;width: 90%; height: 40px; border: 1px solid black;padding: 0px;margin-top:5px"><a href="#'+group_id+'">'+group_name.replace(":","")+'</a></div>'

    if in_table == True: contenido+="</table>" + '\n'
    # Escribir el contenido en un archivo HTML
    fichero_html = os.path.splitext(ruta_fichero)[0] + '.html'

    # Incluye la cabecera y el pie html
    contenido_html = '<html><head>'
    contenido_html +='<style>body {font-family: "Courier New", monospace;} table {width: 100%;border-collapse: collapse;border: 1px solid black;padding: 0;margin: 0;} th {background-color: black;color: white;} td, th {border: 1px solid black;padding: 0;margin: 0;}.container {height: 100vh; display: flex;} .div1 {width: 200px;background-color: #f1f1f1;overflow: hidden;} .div2 {flex-grow: 1;background-color: #ccc;overflow-y: scroll;} .div1 div {min-height: 50px;display: flex;align-items: center;justify-content: left;} .div1 a{text-decoration: none;font-weight: bold;}</style>'
    contenido_html+='</head><body>' + '\n'
    contenido_html += '<div class="container"><div class="div1">' + '\n'
    contenido_html += indice + '\n'
    contenido_html += '</div>' + '\n'
    contenido_html += '<div class="div2">' + '\n'
    contenido_html += contenido + '\n'
    contenido_html += '</div>' + '\n'
    contenido_html += '</div>' + '\n'
    contenido_html += "</body></html>"

    # Guarda el contenido HTML en un fichero
    with open(fichero_html, 'w',encoding='utf-8') as file:
        file.write(contenido_html)

# Función para verificar si el fichero ha cambiado
def verificar_cambios():
    global hash_inicial

    while True:
        # Calcula el hash actual del fichero
        if os.path.exists(config.fichero_con_ruta):
            with open(config.fichero_con_ruta, 'rb') as file:
                contenido = file.read()
                hash_actual = hashlib.md5(contenido).hexdigest()

            if hash_inicial is None:
                hash_inicial = hash_actual
                #Genere el briefing por primera vez
                procesar_fichero(config.fichero_con_ruta)
            elif hash_inicial != hash_actual:
                # Si el hash ha cambiado, llama a la función para procesar el fichero
                procesar_fichero(config.fichero_con_ruta)
                hash_inicial = hash_actual

        time.sleep(1)  # Espera 1 segundo antes de volver a verificar

