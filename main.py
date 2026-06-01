import sqlite3

conexion = sqlite3.connect('roble.db')
cursor = conexion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS producto(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            stock INTEGER NOT NULL,
            precio REAL)
''')

productos_ejemplo = [
    ('DESINFECTANTE', 10, 13550),
    ('JABON', 25, 8500),
    ('CLORO', 40, 5200)
]

cursor.executemany('INSERT INTO producto (nombre, stock, precio) VALUES (?,?,?)', productos_ejemplo)

conexion.commit()
conexion.close()