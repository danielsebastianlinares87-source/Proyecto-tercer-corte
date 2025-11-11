import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt

class Ai_job_market:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.data.columns = self.data.columns.str.strip()

    def imprimir_todo(self):
        print(self.data)

    # -------------------------------------
    # 🔹 NUEVAS FUNCIONES AGREGADAS
    # -------------------------------------

    def buscar(self):
        print("BÚSQUEDA DE OFERTAS")
        palabra = input("Ingrese una palabra clave (empresa, puesto o habilidad): ").lower()
        resultado = self.data[
            self.data["company_name"].str.lower().str.contains(palabra, na=False)
            | self.data["job_title"].str.lower().str.contains(palabra, na=False)
            | self.data["skills_required"].str.lower().str.contains(palabra, na=False)
        ]
        if len(resultado) > 0:
            print(f"Se encontraron {len(resultado)} resultados:")
            print(resultado)
        else:
            print("No se encontraron resultados.")

    def filtrar(self):
        print("FILTRADO DE DATOS")
        columna = input("Ingrese el nombre de la columna por la que desea filtrar (ej. industry, location, experience_level): ").strip()
        valor = input("Ingrese el valor que desea buscar: ").strip().lower()
        if columna in self.data.columns:
            filtrado = self.data[self.data[columna].str.lower().str.contains(valor, na=False)]
            print(f"Se encontraron {len(filtrado)} resultados:")
            print(filtrado)
        else:
            print("Columna no válida.")

    def ordenar(self):
        print("ORDENAR DATOS")
        columna = input("Ingrese la columna por la que desea ordenar (ej. salary_range_usd, posted_date): ").strip()
        if columna in self.data.columns:
            orden = input("¿Desea ordenar ascendente (a) o descendente (d)? ").lower()
            asc = True if orden == "a" else False
            try:
                datos_ordenados = self.data.sort_values(by=columna, ascending=asc)
                print(datos_ordenados.head(10))
            except Exception as e:
                print("Error al ordenar:", e)
        else:
            print("Columna no válida.")

    def exportar(self):
        print("EXPORTAR DATOS")
        nombre_archivo = input("Ingrese el nombre del archivo de destino (sin extensión): ").strip()
        ruta_salida = f"{nombre_archivo}.csv"
        try:
            self.data.to_csv(ruta_salida, index=False)
            print(f"Datos exportados correctamente a {ruta_salida}")
        except Exception as e:
            print("Error al exportar:", e)

    # -------------------------------------
    # 🔹 FUNCIONES CRUD Y ANÁLISIS ORIGINALES
    # -------------------------------------

    def crear(self):
        print("CREAR NUEVA OFERTA")
        try:
            job_id = int(input("Ingrese ID del empleo: "))
            company_name = input("Nombre de la empresa: ")
            industry = input("Industria: ")
            job_title = input("Título del puesto: ")
            skills_required = input("Habilidades requeridas (separadas por comas): ")
            experience_level = input("Nivel de experiencia (Entry/Mid/Senior): ")
            employment_type = input("Tipo de contrato (Full-time/Part-time/Contract/Internship): ")
            location = input("Ubicación (ciudad, país): ")
            salary_range_usd = input("Rango salarial en USD (ej. 50000-80000): ")
            posted_date = input("Fecha de publicación (YYYY-MM-DD): ")
            company_size = input("Tamaño de la empresa (Startup/Medium/Large): ")
            tools_preferred = input("Herramientas preferidas: ")

            nuevo = {
                "job_id": job_id,
                "company_name": company_name,
                "industry": industry,
                "job_title": job_title,
                "skills_required": skills_required,
                "experience_level": experience_level,
                "employment_type": employment_type,
                "location": location,
                "salary_range_usd": salary_range_usd,
                "posted_date": posted_date,
                "company_size": company_size,
                "tools_preferred": tools_preferred
            }

            self.data = pd.concat([self.data, pd.DataFrame([nuevo])], ignore_index=True)
            self.data.to_csv(self.file_path, index=False)
            print("Oferta creada y guardada exitosamente.")
        except Exception as e:
            print("Error al crear oferta:", e)

    def editar(self):
        print("EDITAR OFERTA EXISTENTE")
        try:
            job_id = int(input("Ingrese el ID del empleo que desea editar: "))
            if job_id in self.data["job_id"].values:
                print("Oferta encontrada:")
                print(self.data[self.data["job_id"] == job_id])
                columna = input("Ingrese el nombre de la columna que desea editar: ").strip()
                if columna in self.data.columns:
                    nuevo_valor = input(f"Ingrese el nuevo valor para '{columna}': ")
                    self.data.loc[self.data["job_id"] == job_id, columna] = nuevo_valor
                    self.data.to_csv(self.file_path, index=False)
                    print("Registro actualizado correctamente.")
                else:
                    print("Columna no válida.")
            else:
                print("No se encontró ningún empleo con ese ID.")
        except Exception as e:
            print("Error al editar oferta:", e)

    def eliminar(self):
        print("ELIMINAR OFERTA")
        try:
            job_id = int(input("Ingrese el ID del empleo que desea eliminar: "))
            if job_id in self.data["job_id"].values:
                confirm = input("¿Está seguro de eliminar este registro? (s/n): ").lower()
                if confirm == "s":
                    self.data = self.data[self.data["job_id"] != job_id]
                    self.data.to_csv(self.file_path, index=False)
                    print("Registro eliminado correctamente.")
                else:
                    print("Operación cancelada.")
            else:
                print("No se encontró ningún empleo con ese ID.")
        except Exception as e:
            print("Error al eliminar oferta:", e)

    # Las funciones analíticas se mantienen igual (del 1 al 17)
    # ... (todo tu bloque "menu_analisis" y demás va aquí sin cambios)

    # -------------------------------------
    # 🔹 MENÚ PRINCIPAL CLI
    # -------------------------------------

archivo = r"C:\Users\ADMIN\Downloads\Proyecto tercer corte\4. ai_job_market.csv"

ai = Ai_job_market(archivo)

print("Bienvenido al Centro de Ofertas Laborales de IA")

while True:
    print("\nSeleccione una opción:")
    print("1. Mostrar datos")
    print("2. Crear oferta")
    print("3. Editar oferta")
    print("4. Eliminar oferta")
    print("5. Buscar ofertas")
    print("6. Filtrar datos")
    print("7. Ordenar registros")
    print("8. Exportar CSV")
    print("9. Análisis y estadísticas")
    print("10. Salir")

    opcion = input("Ingrese su opción: ")

    if opcion == "1":
        ai.imprimir_todo()
    elif opcion == "2":
        ai.crear()
    elif opcion == "3":
        ai.editar()
    elif opcion == "4":
        ai.eliminar()
    elif opcion == "5":
        ai.buscar()
    elif opcion == "6":
        ai.filtrar()
    elif opcion == "7":
        ai.ordenar()
    elif opcion == "8":
        ai.exportar()
    elif opcion == "9":
        ai.menu_analisis()
    elif opcion == "10":
        print("Saliendo del sistema...")
        break
    else:
        print("Opción inválida, intente nuevamente.")

