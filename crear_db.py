import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT UNIQUE NOT NULL,
    tipo TEXT NOT NULL,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    cedula TEXT NOT NULL,
    celular TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Base de datos y tabla creada exitosamente.")
