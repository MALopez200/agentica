import sqlite3

conexion = sqlite3.connect('roble.db')
cursor = conexion.cursor()

# Añadir columnas a producto (solo si no existen)
try:
    cursor.execute("ALTER TABLE producto ADD COLUMN categoria TEXT")
except sqlite3.OperationalError:
    pass  # ya existe

try:
    cursor.execute("ALTER TABLE producto ADD COLUMN proveedor TEXT")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE producto ADD COLUMN stock_minimo INTEGER DEFAULT 5")
except sqlite3.OperationalError:
    pass

# Crear tabla ventas
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES producto(id)
)
''')

conexion.commit()
conexion.close()
print("Base de datos actualizada.")