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

    def menu_analisis(self):
        print("ANÁLISIS Y ESTADÍSTICAS")
        print("1. Cantidad total de ofertas registradas")
        print("2. Industria con mayor número de empresas activas")
        print("3. Número de ofertas por industria")
        print("4. Número de ofertas por nivel de experiencia")
        print("5. Número de ofertas por tipo de contrato")
        print("6. Promedio del rango salarial")
        print("7. Top 5 cargos más comunes")
        print("8. Top 5 empresas con más ofertas publicadas")
        print("9. Ofertas con salario máximo y mínimo")
        print("10. Cantidad de ofertas que requieren habilidades específicas")
        print("11. Cantidad de ofertas por ciudad")
        print("12. Número de habilidades más demandadas")
        print("13. Cantidad de ofertas según el tamaño de la empresa")
        print("14. Salario promedio estimado por nivel de experiencia")
        print("15. Cantidad de ofertas publicadas por año")

        opcion = input("Seleccione una opción (1-15) o 'b' para volver: ")
        if opcion == "b":
            return

        try:
            if opcion == "1":
                total = len(self.data)
                print("Cantidad total de ofertas:", total)
                plt.bar(["Total Ofertas"], [total])
                plt.title("Cantidad total de ofertas registradas")
                plt.show()

            elif opcion == "2":
                industria_top = self.data["industry"].mode()[0]
                print("Industria con mayor número de empresas activas:", industria_top)
                conteo = self.data["industry"].value_counts()
                conteo.plot(kind="bar", title="Ofertas por industria")
                plt.show()

            elif opcion == "3":
                conteo = self.data["industry"].value_counts()
                print(conteo)
                conteo.plot(kind="barh", title="Número de ofertas por industria")
                plt.show()

            elif opcion == "4":
                niveles = self.data["experience_level"].value_counts()
                print(niveles)
                niveles.plot(kind="pie", autopct="%1.1f%%", title="Ofertas por nivel de experiencia")
                plt.ylabel("")
                plt.show()

            elif opcion == "5":
                tipos = self.data["employment_type"].value_counts()
                print(tipos)
                tipos.plot(kind="bar", title="Ofertas por tipo de contrato")
                plt.show()

            elif opcion == "6":
                def promedio_salarial(s):
                    try:
                        partes = list(map(int, s.split("-")))
                        return sum(partes) / len(partes)
                    except:
                        return None
                salarios = list(filter(None, map(promedio_salarial, self.data["salary_range_usd"])))
                promedio = sum(salarios) / len(salarios) if salarios else 0
                print("Promedio del rango salarial en USD:", round(promedio, 2))
                plt.hist(salarios, bins=10)
                plt.title("Distribución de salarios promedio")
                plt.xlabel("Salario USD")
                plt.ylabel("Frecuencia")
                plt.show()

            elif opcion == "7":
                top = self.data["job_title"].value_counts().head(5)
                print(top)
                top.plot(kind="bar", title="Top 5 cargos más comunes")
                plt.show()

            elif opcion == "8":
                top_empresas = self.data["company_name"].value_counts().head(5)
                print(top_empresas)
                top_empresas.plot(kind="bar", title="Top 5 empresas con más ofertas")
                plt.show()

            elif opcion == "9":
                def rango(s):
                    try:
                        partes = list(map(int, s.split("-")))
                        return max(partes)
                    except:
                        return None
                self.data["salario_max"] = list(map(rango, self.data["salary_range_usd"]))
                maximo = self.data[self.data["salario_max"] == self.data["salario_max"].max()]
                minimo = self.data[self.data["salario_max"] == self.data["salario_max"].min()]
                print("Ofertas con salario máximo:")
                print(maximo[["job_title", "company_name", "salary_range_usd"]])
                print("Ofertas con salario mínimo:")
                print(minimo[["job_title", "company_name", "salary_range_usd"]])
                valores = [minimo["salario_max"].min(), maximo["salario_max"].max()]
                plt.bar(["Mínimo", "Máximo"], valores)
                plt.title("Comparación salario máximo vs mínimo")
                plt.show()

            elif opcion == "10":
                habilidad = input("Ingrese una habilidad para buscar: ").lower()
                conteo = len(list(filter(lambda x: habilidad in str(x).lower(), self.data["skills_required"])))
                print("Cantidad de ofertas que requieren", habilidad + ":", conteo)
                plt.bar([habilidad], [conteo])
                plt.title("Ofertas que requieren la habilidad ingresada")
                plt.show()

            elif opcion == "11":
                ciudades = self.data["location"].value_counts()
                print(ciudades)
                ciudades.head(10).plot(kind="barh", title="Top 10 ciudades con más ofertas")
                plt.show()

            elif opcion == "12":
                habilidades = self.data["skills_required"].dropna().apply(lambda x: [h.strip().lower() for h in x.split(",")])
                todas = reduce(lambda a, b: a + b, habilidades)
                top = pd.Series(todas).value_counts().head(10)
                print("Habilidades más demandadas:")
                print(top)
                top.plot(kind="bar", title="Top 10 habilidades más demandadas")
                plt.show()

            elif opcion == "13":
                tamaños = self.data["company_size"].value_counts()
                print(tamaños)
                tamaños.plot(kind="pie", autopct="%1.1f%%", title="Ofertas por tamaño de empresa")
                plt.ylabel("")
                plt.show()

            elif opcion == "14":
                def prom_salarial_fila(s):
                    try:
                        partes = list(map(int, s.split("-")))
                        return sum(partes) / len(partes)
                    except:
                        return None
                self.data["prom_salario"] = list(map(prom_salarial_fila, self.data["salary_range_usd"]))
                resultado = self.data.groupby("experience_level")["prom_salario"].mean()
                print(resultado)
                resultado.plot(kind="bar", title="Salario promedio por nivel de experiencia")
                plt.show()

            elif opcion == "15":
                self.data["posted_date"] = pd.to_datetime(self.data["posted_date"], errors="coerce")
                conteo_anual = self.data["posted_date"].dt.year.value_counts().sort_index()
                print(conteo_anual)
                conteo_anual.plot(kind="line", marker="o", title="Ofertas publicadas por año")
                plt.xlabel("Año")
                plt.ylabel("Cantidad de ofertas")
                plt.show()

            else:
                print("Opción inválida.")

        except Exception as e:
            print("Error durante el análisis:", e)


archivo = r"C:\Users\ADMIN\Downloads\Proyecto tercer corte\4. ai_job_market.csv"

ai = Ai_job_market(archivo)

print("Bienvenido al Centro de Ofertas Laborales de IA")

while True:
    print("\nSeleccione una opción:")
    print("1. Mostrar datos")
    print("2. Crear oferta")
    print("3. Editar oferta")
    print("4. Eliminar oferta")
    print("5. Análisis y estadísticas")
    print("6. Salir")

    opcion = input(" Ingrese su opción: ")

    if opcion == "1":
            ai.imprimir_todo()
    elif opcion == "2":
            ai.crear()
    elif opcion == "3":
            ai.editar()
    elif opcion == "4":
            ai.eliminar()
    elif opcion == "5":
            ai.menu_analisis()
    elif opcion == "6":
            print(" Saliendo del sistema...")
            break
    else:
            print(" Opción inválida, intente nuevamente.")

