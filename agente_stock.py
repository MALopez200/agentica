import ollama
import sqlite3
from unidecode import unidecode
import json

conexion = sqlite3.connect('roble.db')
cursor  = conexion.cursor()

cursor.execute('''
SELECT nombre FROM producto
''')

productos = [unidecode(fila[0].lower()) for fila in cursor.fetchall()]
lista_productos = ', '.join(productos)

correo = "Hola, ¿tienen desinfectante? Necesito 5 litros."

prompt = f"Eres un asistente que extrae el producto de un correo de cliente. Lista de productos disponibles: {lista_productos}. Si en el correo se menciona alguno de esos productos, debes responder ÚNICAMENTE con un JSON que contenga la clave \"producto\" y el valor exactamente como aparece en la lista (todo en minúsculas y sin acentos). Ejemplo: si el correo dice '¿tienen desinfectante?' y 'desinfectante' está en la lista, responde {{\"producto\": \"desinfectante\"}}. Si no se menciona ningún producto de la lista, responde {{\"tipo\": \"no_stock\"}}. No añadas texto adicional ni uses comillas simples."

respuesta = ollama.chat(
    model= 'llama3.2:latest', 
    messages=[
        {'role':'system','content':prompt},
        {'role':'user','content':correo}
    ])

contenido = respuesta['message']['content']

inicio = contenido.find('{')
fin = contenido.find('}')

if inicio != -1 and fin != -1:
    json_str = contenido[inicio:fin+1]
else:
    json_str = ''

try:
    datos = json.loads(json_str)
except json.JSONDecodeError:
    datos = {'tipo': 'error', 'mensaje': 'JSON no valido'}

if 'producto' in datos:
    producto_buscado = datos['producto']
    cursor.execute(
        "SELECT nombre, stock FROM producto WHERE LOWER(nombre) LIKE ?",
        ('%' + producto_buscado + '%',)
    )
    resultado = cursor.fetchone()
    
    if resultado:
        print(f"Producto encontrado: {resultado[0]} - Stock: {resultado[1]}")
    else:
        print(f"Producto '{producto_buscado}' no encontrado en la base de datos.")
else:
    print("El correo no es una consulta de stock.")

if resultado:
    nombre_producto = resultado[0]
    stock_producto = resultado[1]

    prompt_respuesta = f"Eres un asistente de atención al cliente de una distribuidora de productos de limpieza. Tu tarea es redactar un correo electrónico profesional y cordial respondiendo a una consulta de stock."

    mensaje_usuario = f"El cliente preguntó por '{nombre_producto}'. Tenemos {stock_producto} unidades disponibles. Redacta un correo de respuesta breve, agradeciendo el interés e indicando el stock disponible."

    respuesta_correo = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': prompt_respuesta},
            {'role': 'user', 'content': mensaje_usuario}
        ]
    )

    print("\n📧 Correo generado:\n")
    print(respuesta_correo['message']['content'])

conexion.close()