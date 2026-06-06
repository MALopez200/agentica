import ollama
import sqlite3
import json
import time
from unidecode import unidecode
from clasificador import clasificar_correo
from extractor import extraer_producto
from redactor import generar_respuesta

conexion = sqlite3.connect('roble.db')
cursor = conexion.cursor()

correos_pendientes = ['hola tienen jabon pino 20l', 'cual es su horario de atencion', 'tienen servicio a domicilio?', 'necesito 300 unidades de cloro citrico spray', 'estan contratando personal?']

# Ciclo para automatizacion
while True:
    #Revision de nuevos correos
    if correos_pendientes:
        correo = correos_pendientes.pop(0)
        print('Tienes correos por revisar')
    # clasificar correos
        categoria = clasificar_correo(correo)
        print('Categoria del correo', categoria)
    
        if 'stock' in categoria:
            producto = extraer_producto(correo)
            if producto:
                # buscar en BD
                cursor.execute("SELECT nombre, stock FROM producto WHERE LOWER(nombre) LIKE ?", ('%' + producto + '%',))
                resultado = cursor.fetchone()
                if resultado:
                    nombre_prod, stock = resultado
                    respuesta = generar_respuesta(nombre_prod, stock)
                    print("Respuesta generada:\n", respuesta)
                else:
                    print("Producto no encontrado en inventario.")
            else:
                print("No se pudo extraer el producto del correo.")
        else:
            print('→ Requiere revisión humana')
    else:
        print('No tienes correos por revisar')
        
        time.sleep(5)    

    time.sleep(2)

    conexion.close()