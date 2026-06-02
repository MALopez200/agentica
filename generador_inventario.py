import sqlite3
import time
import random

conexion = sqlite3.connect('roble.db')
cursor = conexion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS producto(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE,
            stock INTEGER NOT NULL,
            precio REAL)
''')


tipos = ['Desinfectante', 'Jabón', 'Cloro', 'Limpiador', 'Quitamanchas']
aromas = ['Lavanda', 'Pino', 'Neutro', 'Cítrico', 'Eucalipto']
formatos = ['1L', '5L', '20L', 'Spray 500ml', 'Gel 750ml']


while True:

    tipo_aleatorio = random.choice(tipos)
    aroma_aleatorio = random.choice(aromas)
    formato_aleatorio = random.choice(formatos)

    nombre = f'{tipo_aleatorio} {aroma_aleatorio} {formato_aleatorio}'
    stock = random.randint(1,10)
    precio = random.uniform(5000.00, 50000.00)

    cursor.execute('''
        INSERT INTO producto (nombre,stock,precio)
        VALUES (?,?,?)
        ON CONFLICT (nombre) DO UPDATE SET
        stock = stock + excluded.stock,
        precio = excluded.precio
        ''', (nombre,stock,precio))
    
    conexion.commit()

    print(f'se ha agregado {nombre} al inventario')

    time.sleep(1)