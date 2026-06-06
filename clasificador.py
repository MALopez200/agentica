import ollama

def clasificar_correo(correo):
    # se crea el prompt 
    prompt = """Eres un clasificador de correos de una distribuidora de productos de limpieza. Solo debes responder con UNA de estas palabras exactas: "stock", "pedido", "queja", "otro".
    Ejemplos:
    - Si el correo pregunta por disponibilidad de algún producto: "stock"
    - Si el correo pide hacer un pedido o comprar: "pedido"
    - Si el correo expresa insatisfacción: "queja"
    - Si es una consulta de horarios, servicios, empleo o cualquier otra cosa: "otro"
    No escribas ninguna explicación, solo la palabra exacta."""
    # Se llama al modelo para el analisis del prompt
    respuesta = ollama.chat(
    model= 'llama3.2:latest', 
    messages=[
    {'role':'system','content':prompt},
    {'role':'user','content':correo}
    ])
    categoria = respuesta['message']['content'].strip().lower()
    return categoria