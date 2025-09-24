import sqlite3
import csv
import os

# ====================================
# 🔹 Conexión a la base de datos
# ====================================
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
CREATE TABLE IF NOT EXISTS bautizos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    s TEXT,
    libro TEXT,
    partida TEXT,
    nombres TEXT,
    apellidos TEXT,
    parroquia TEXT,
    edad TEXT,
    padre TEXT,
    madre TEXT,
    pm TEXT,
    padrino TEXT,
    madrina TEXT,
    fecha DATE
)
)
conn.commit()

# ====================================
# 🔹 Función: Importar CSV → SQLite
# ====================================
def importar_csv():
    try:
        folder = "data/"
        archivos = [f for f in os.listdir(folder) if f.endswith(".csv")]

        if not archivos:
            print("⚠️ No se encontraron archivos CSV en la carpeta data.\n")
            return

        for file in archivos:
            print(f"📂 Importando archivo: {file}...")
            with open(os.path.join(folder, file), newline='', encoding="latin-1") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        # Limpiar espacios en encabezados
                        row = {k.strip(): v.strip() for k, v in row.items()}

                        # Construir fecha YYYY-MM-DD
                        dia = row.get("DIA", "").zfill(2)
                        mes = row.get("MES", "").zfill(2)
                        anio = row.get("AÑO", row.get("ANO", ""))  # soporte por si no reconoce Ñ
                        fecha = f"{anio}-{mes}-{dia}" if anio and mes and dia else None

                        cursor.execute("""
                            INSERT INTO bautizos (genero, libro, partida, nombres, apellidos,
                                                  parroquia, edad, padre, madre, pm, padrino, madrina, fecha)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row.get("S", ""),
                            row.get("LIBRO", ""),
                            row.get("Partida", ""),
                            row.get("NOMBRES", ""),
                            row.get("APELLIDOS", ""),
                            row.get("PARROQUIA DE BAUTIZO", ""),
                            row.get("EDAD", ""),
                            row.get("PADRE", ""),
                            row.get("MADRE", ""),
                            row.get("P/M", ""),
                            row.get("PADRINO", ""),
                            row.get("MADRINA", ""),
                            fecha
                        ))
                    except Exception as e:
                        print(f"⚠️ Error importando fila: {row}")
                        print(f"   Detalle: {e}")
            conn.commit()
            print(f"✅ Datos de {file} importados correctamente.\n")

    except Exception as e:
        print(f"❌ Error general al importar: {e}\n")

# ====================================
# 🔹 Función: Buscar por nombre
# ====================================
def buscar_por_nombre():
    try:
        nombre = input("Ingrese el nombre o apellido a buscar: ")
        cursor.execute("""
            SELECT id, nombres, apellidos, fecha, padre, madre, padrino, madrina
            FROM bautizos WHERE nombres LIKE ? OR apellidos LIKE ?
        """, (f"%{nombre}%", f"%{nombre}%"))
        resultados = cursor.fetchall()

        if resultados:
            print("\n🔎 RESULTADOS DE LA BÚSQUEDA:")
            for r in resultados:
                print(f"ID: {r[0]} | {r[1]} {r[2]} | Fecha: {r[3]} | Padres: {r[4]} y {r[5]} | Padrinos: {r[6]} y {r[7]}")
            print()
        else:
            print("⚠️ No se encontraron coincidencias.\n")
    except Exception as e:
        print(f"❌ Error al buscar: {e}\n")

# ====================================
# 🔹 Menú principal
# ====================================
def menu():
    while True:
        print("===== MENÚ PRINCIPAL =====")
        print("1. Importar archivos CSV")
        print("2. Buscar por nombre o apellido")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            importar_csv()
        elif opcion == "2":
            buscar_por_nombre()
        elif opcion == "3":
            print("👋 Saliendo del programa...")
            break
        else:
            print("❌ Opción no válida\n")

# ====================================
# 🔹 Ejecutar menú
# ====================================
if __name__ == "__main__":
    menu()
    conn.close()
