import ollama

def generar_respuesta(nombre_producto, stock_producto):

    prompt_respuesta = f"Eres un asistente de atención al cliente de una distribuidora de productos de limpieza. Redacta un correo electrónico breve y cordial respondiendo a una consulta de stock. Usa 'Estimado cliente' como saludo y 'Atentamente, El Roble' como despedida. No uses marcadores como [Nombre del cliente] o [Tu nombre]."

    mensaje_usuario = f"El cliente preguntó por '{nombre_producto}'. Tenemos {stock_producto} unidades disponibles. Redacta un correo de respuesta breve, agradeciendo el interés e indicando el stock disponible."

    respuesta_correo = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': prompt_respuesta},
            {'role': 'user', 'content': mensaje_usuario}
                ]
            )

    return respuesta_correo['message']['content']