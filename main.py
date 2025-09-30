2import os
import csv
import sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")
def crear_tabla():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bautizos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genero TEXT,
            libro TEXT,
            partida TEXT,
            nombres TEXT,
            apellidos TEXT,
            parroquia_de_bautizo TEXT,
            edad INTEGER,
            padre TEXT,
            madre TEXT,
            p_m TEXT,
            padrino TEXT,
            madrina TEXT,
            fecha_de_bautizo TEXT,
            dia INTEGER,
            mes INTEGER,
            anio INTEGER
        );
    """)
    conn.commit()
    conn.close()

def importar_csv():
    if not os.path.exists(DATA_DIR):
        print(f" La carpeta 'data' no existe en {BASE_DIR}.")
        return

    archivos = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    if not archivos:
        print(" No hay archivos CSV en la carpeta 'data'.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for archivo in archivos:
        ruta = os.path.join(DATA_DIR, archivo)
        print(f" Importando {ruta}...")

        try:
            # Detectar encoding automáticamente
            try:
                f = open(ruta, "r", encoding="utf-8")
                f.read(1)
                f.seek(0)
            except UnicodeDecodeError:
                f = open(ruta, "r", encoding="latin1")

            with f:
                reader = csv.DictReader(f)
                # Normalizar nombres de columnas
                reader.fieldnames = [col.strip().lower().replace(" ", "_") for col in reader.fieldnames]

                for row in reader:
                    cur.execute("""
                        INSERT INTO bautizos (
                            genero, libro, partida, nombres, apellidos, parroquia_de_bautizo,
                            edad, padre, madre, p_m, padrino, madrina,
                            fecha_de_bautizo, dia, mes, anio
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row.get("s"),
                        row.get("libro"),
                        row.get("partida"),
                        row.get("nombres"),
                        row.get("apellidos"),
                        row.get("parroquia_de_bautizo"),
                        row.get("edad"),
                        row.get("padre"),
                        row.get("madre"),
                        row.get("p/m"),
                        row.get("padrino"),
                        row.get("madrina"),
                        row.get("fecha_de_bautizo"),
                        row.get("dia"),
                        row.get("mes"),
                        row.get("año")
                    ))
            conn.commit()
        except Exception as e:
            print(f" Error al importar {archivo}: {e}")

    conn.close()
    print("✅ Importación completada.")
def buscar_por_nombre(nombre):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM bautizos WHERE nombres LIKE ?", ('%' + nombre + '%',))
    resultados = cur.fetchall()
    conn.close()

    if resultados:
        print("\n Resultados encontrados:")
        for r in resultados:
            print(r)
    else:
        print("\n No se encontraron resultados.")
def main():
    crear_tabla()

    while True:
        print("\n Menú Principal")
        print("1. Importar CSV")
        print("2. Buscar por nombre")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            importar_csv()
        elif opcion == "2":
            nombre = input("Ingrese el nombre a buscar: ")
input("\nPresiona Enter para salir...")
