import ollama
import sqlite3
from unidecode import unidecode

conexion = sqlite3.connect('roble.db')
cursor  = conexion.cursor()

cursor.execute('''
SELECT nombre FROM producto
''')

productos = [unidecode(fila[0].lower()) for fila in cursor.fetchall()]
lista_productos = ', '.join(productos)

correo = "Hola, ¿tienen desinfectante? Necesito 5 litros."

prompt = f"Eres un asistente que extrae el producto consultado de un correo. Los productos disponibles son: {lista_productos}. Solo debes responder en JSON. Si el correo pregunta por stock de un producto,  devuelve {{'producto': 'nombre exacto producto'}}. Si no, devuelve {{'tipo': 'no_stock'}}."

respuesta = ollama.chat(
    model= 'llama3.2:latest', 
    messages=[
        {'role':'system','content':prompt},
        {'role':'user','content':correo}
    ])

print(respuesta['message']['content'])

conexion.close()