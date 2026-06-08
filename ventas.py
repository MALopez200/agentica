import sqlite3
from datetime import datetime

def procesar_pedido(datos_pedido, cursor):

    producto = datos_pedido.get('producto')
    cantidad = datos_pedido.get('cantidad')

    if producto is None or cantidad is None:
        return "Error: el producto y la cantidad son obligatorios."

    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return "Error: la cantidad proporcionada no es un número válido."

    cursor.execute(
        "SELECT id, stock, precio FROM producto WHERE LOWER(nombre) LIKE ?",
        ('%' + producto + '%',)
    )
    fila = cursor.fetchone()

    if fila is None:
        return f"Producto '{producto}' no encontrado."
    
    id_producto = fila[0]
    stock_actual = fila[1]
    precio_unitario = fila[2]

    if stock_actual < cantidad:
        return f"Stock insuficiente. Solo quedan {stock_actual} unidades."
    
    nuevo_stock = stock_actual - cantidad
    cursor.execute("UPDATE producto SET stock = ? WHERE id = ?", (nuevo_stock, id_producto))

    fecha = datetime.now().isoformat()
    total = cantidad * precio_unitario
    cursor.execute(
        "INSERT INTO ventas (fecha, producto_id, cantidad, precio_unitario, total) VALUES (?, ?, ?, ?, ?)",
        (fecha, id_producto, cantidad, precio_unitario, total)
    )
    cursor.connection.commit()

    return f"✅ Pedido confirmado: {cantidad} unidad(es) de '{producto}' por un total de ${total:.2f}."
