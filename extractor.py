import sqlite3
import ollama
import json
from unidecode import unidecode

conexion = sqlite3.connect('roble.db')
cursor = conexion.cursor()

def extraer_producto(correo):

    cursor.execute('SELECT nombre FROM producto')
    producto_db = [unidecode(fila[0].lower()) for fila in cursor.fetchall()]

    if not producto_db:
        return None 
    
    lista_productos = ','.join(producto_db)

    prompt = f"Eres un asistente que extrae el producto de un correo de cliente. Lista de productos disponibles: {lista_productos}. Si en el correo se menciona alguno de esos productos, debes responder ÚNICAMENTE con un JSON que contenga la clave \"producto\" y el valor exactamente como aparece en la lista (todo en minúsculas y sin acentos). Ejemplo: si el correo dice '¿tienen desinfectante?' y 'desinfectante' está en la lista, responde {{\"producto\": \"desinfectante\"}}. Si no se menciona ningún producto de la lista, responde {{\"tipo\": \"no_stock\"}}. No añadas texto adicional ni uses comillas simples."

    respuesta = ollama.chat(
    model= 'llama3.2:latest', 
    messages=[
        {'role':'system','content':prompt},
        {'role':'user','content':correo}
        ]
    )

    contenido = respuesta['message']['content']

    inicio = contenido.find('{')
    fin = contenido.find('}')

    if inicio != -1 and fin != -1:
        json_str = contenido[inicio:fin+1]
    else:
        json_str = ''

    try:
        datos = json.loads(json_str)
        return datos.get('producto')
    except json.JSONDecodeError:
        return None