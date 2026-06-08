import sqlite3
import pandas as pd  # Importamos pandas con el alias 'pd' (es el estándar)

# 1. Conectamos a la base de datos
conexion = sqlite3.connect('roble.db')

# 2. Le pedimos a Pandas que lea las tablas directamente con consultas SQL
df_productos = pd.read_sql_query("SELECT id, nombre, stock, precio, categoria, stock_minimo FROM producto", conexion)
df_ventas = pd.read_sql_query("SELECT id, producto_id, cantidad, total FROM ventas", conexion)

# 3. Cerramos la conexión (Pandas ya guardó los datos en su memoria)
conexion.close()

# ... (deja los puntos 1, 2 y 3 igual) ...

# 4. FUSIONAR TABLAS (El "Merge")
# Unimos las ventas con los productos usando el ID del producto como puente
df_completo = pd.merge(df_ventas, df_productos, left_on='producto_id', right_on='id')

# 5. AGRUPAR Y SUMAR (Ventas por Categoría)
# Agrupamos por la columna 'categoria' y sumamos la columna 'total' de las ventas
ventas_por_categoria = df_completo.groupby('categoria')['total'].sum().reset_index()

# 6. FILTRAR DATOS (Alerta de Stock Mínimo)
# Filtramos los productos cuyo stock actual sea menor que su stock_minimo
alertas_stock = df_productos[df_productos['stock'] < df_productos['stock_minimo']]

# 7. Mostramos los resultados analizados en la terminal
print("💰 --- VENTAS TOTALES POR CATEGORÍA ---")
print(ventas_por_categoria)

print("\n🚨 --- ALERTAS DE REPOSICIÓN (STOCK BAJO) ---")
if not alertas_stock.empty:
    print(alertas_stock[['nombre', 'stock', 'stock_minimo']])
else:
    print("¡Todo perfecto! No hay productos con stock bajo.")