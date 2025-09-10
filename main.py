import sqlite3
conn = sqlite3.connect("bautizos.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bautizos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha DATE NOT NULL,
    padre TEXT,
    madre TEXT,
    padrino TEXT,
    madrina TEXT
)
""")
conn.commit()

def agregar_bautizo():
    nombre = input("Nombre del bautizado: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    padre = input("Nombre del padre: ")
    madre = input("Nombre de la madre: ")
    padrino = input("Nombre del padrino: ")
    madrina = input("Nombre de la madrina: ")

    cursor.execute("INSERT INTO bautizos (nombre, fecha, padre, madre, padrino, madrina) VALUES (?, ?, ?, ?, ?, ?)",
                   (nombre, fecha, padre, madre, padrino, madrina))
    conn.commit()
    print("Registro agregado con éxito.\n")

def listar_bautizos():
    cursor.execute("SELECT id, nombre, fecha FROM bautizos")
    registros = cursor.fetchall()
    if not registros:
        print(" No hay registros.\n")
    else:
        for r in registros:
            print(f"ID: {r[0]} | Nombre: {r[1]} | Fecha: {r[2]}")
        print()

def buscar_bautizo():
    nombre = input("Ingrese el nombre a buscar: ")
    cursor.execute("SELECT * FROM bautizos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    resultados = cursor.fetchall()
    if not resultados:
        print(" No se encontraron registros.\n")
    else:
        for r in resultados:
            print(r)
        print()

# Menú principal
def menu():
    while True:
        print("=== Sistema de Certificados de Bautizo ===")
        print("1. Agregar bautizo")
        print("2. Listar bautizos")
        print("3. Buscar bautizo")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_bautizo()
        elif opcion == "2":
            listar_bautizos()
        elif opcion == "3":
            buscar_bautizo()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida, intente de nuevo.\n")

menu()
conn.close()
