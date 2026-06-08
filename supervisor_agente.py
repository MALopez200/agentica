import ollama
import sqlite3
import json
import time
from unidecode import unidecode
from clasificador import clasificar_correo
from extractor import extraer_producto
from redactor import generar_respuesta
from extractor import extraer_pedido
from ventas import procesar_pedido

conexion = sqlite3.connect('roble.db')
cursor = conexion.cursor()

correos_pendientes = ["necesito 3 limpiador pino 5L"]

# Ciclo para automatizacion
while True:
    # 1. Si no hay correos, esperamos y volvemos a empezar
    if not correos_pendientes:
        print('No tienes correos por revisar')
        time.sleep(5)    
        continue  # <-- Salta al inicio del while a esperar más correos

    # 2. Tomamos el correo
    correo = correos_pendientes.pop(0)
    print('\n📩 Tienes un correo por revisar:', correo)
    
    # 3. Clasificamos
    categoria = clasificar_correo(correo)
    print('Categoria del correo:', categoria)

    # 4. ¿Es revisión humana? (Si no es stock ni pedido, terminamos rápido)
    if 'stock' not in categoria and 'pedido' not in categoria:
        print('→ Requiere revisión humana')
        time.sleep(2)
        continue  # <-- Terminamos con este correo, vamos al siguiente

    # 5. Camino para STOCK
    if 'stock' in categoria:
        producto = extraer_producto(correo, cursor)
        if not producto:
            print("⚠️ No se pudo extraer el producto.")
            continue  # <-- Error, al siguiente correo
            
        cursor.execute("SELECT nombre, stock FROM producto WHERE LOWER(nombre) LIKE ?", ('%' + producto + '%',))
        resultado = cursor.fetchone()
        if not resultado:
            print("⚠️ Producto no encontrado en inventario.")
            continue  # <-- Error, al siguiente correo
            
        nombre_prod, stock = resultado
        respuesta = generar_respuesta(nombre_prod, stock)
        print("Respuesta generada:\n", respuesta)

    # 6. Camino para PEDIDO
    if 'pedido' in categoria:
        datos_pedido = extraer_pedido(correo, cursor)
        if datos_pedido is None or 'error' in datos_pedido:
            print("⚠️ No se pudo entender el pedido.")
            continue  # <-- Error, al siguiente correo
            
        resultado = procesar_pedido(datos_pedido, cursor)
        print(resultado)

    time.sleep(2)