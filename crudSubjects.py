from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
from asignatura import Asignatura
from nivel import Nivel
import time

class CrudSubjects(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/subjects.json')
        self.niveles_json_file = JsonFile(f'{path}/levels.json')
        self.valida = Valida()

    def create(self):
        """Crea una nueva asignatura y la guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['id'], s['descripcion'], s['nivel'], s['active']) for s in data]

        if asignaturas:
            id = max([asignatura.id for asignatura in asignaturas]) + 1
        else:
            id = 1

        descripcion = self.valida.solo_letras("Ingrese la descripción de la asignatura: ", "Descripción inválida. Solo se permiten letras.")

        # Obtener niveles disponibles (solo los activos)
        niveles_data = self.niveles_json_file.read()
        niveles = [Nivel(n['id'], n['nivel']) for n in niveles_data]
        niveles_activos = [nivel for nivel in niveles if nivel.active]

        if not niveles_activos:
            print(f"{yellow_color}No hay niveles activos registrados. Debe crear un nivel antes de crear una asignatura.{reset_color}")
            time.sleep(2)
            return

        print("\nNiveles disponibles:")
        for nivel in niveles_activos:
            print(f"ID: {nivel.id}, Nivel: {nivel.nivel}")

        # Solicitar al usuario que elija un nivel válido
        while True:
            nivel_id = self.valida.solo_numeros("Ingrese el ID del nivel: ", "ID de nivel inválido. Ingrese un número entero positivo.")
            nivel_seleccionado = next((n for n in niveles_activos if n.id == int(nivel_id)), None)
            if nivel_seleccionado:
                break
            else:
                print("Nivel no encontrado o inactivo. Intente de nuevo.")

        nueva_asignatura = Asignatura(id, descripcion, nivel_seleccionado, True)
        asignaturas.append(nueva_asignatura)

        data = [asignatura.__dict__ for asignatura in asignaturas]
        self.json_file.save(data)
        print("Asignatura creada exitosamente.")
        time.sleep(2)

    def update(self):
        """Actualiza una asignatura existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['id'], s['descripcion'], s['nivel'], s['active']) for s in data]

        id = self.valida.solo_numeros("Ingrese el ID de la asignatura a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        asignatura = next((a for a in asignaturas if a.id == int(id)), None)

        if asignatura:
            asignatura.descripcion = self.valida.solo_letras("Ingrese la nueva descripción de la asignatura: ", "Descripción inválida. Solo se permiten letras.")

            # Obtener niveles disponibles (solo los activos)
            niveles_data = self.niveles_json_file.read()
            niveles = [Nivel(n['id'], n['nivel']) for n in niveles_data]
            niveles_activos = [nivel for nivel in niveles if nivel.active]

            if not niveles_activos:
                print(f"{yellow_color}No hay niveles activos registrados. No se puede actualizar el nivel de la asignatura.{reset_color}")
            else:
                print("\nNiveles disponibles:")
                for nivel in niveles_activos:
                    print(f"ID: {nivel.id}, Nivel: {nivel.nivel}")

                # Solicitar al usuario que elija un nivel válido
                while True:
                    nivel_id = self.valida.solo_numeros("Ingrese el ID del nuevo nivel: ", "ID de nivel inválido. Ingrese un número entero positivo.")
                    nivel_seleccionado = next((n for n in niveles_activos if n.id == int(nivel_id)), None)
                    if nivel_seleccionado:
                        break
                    else:
                        print("Nivel no encontrado o inactivo. Intente de nuevo.")

                asignatura.nivel = nivel_seleccionado

            # Convertir los objetos Asignatura de vuelta a diccionarios para guardarlos en el JSON
            data = [asignatura.__dict__ for asignatura in asignaturas]
            self.json_file.save(data)
            print("Asignatura actualizada exitosamente.")
            time.sleep(2)
        else:
            print("Asignatura no encontrada.")
            time.sleep(2)

    def delete(self):
        """Elimina una asignatura del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Asignatura '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['id'], s['descripcion'], s['nivel'], s['active']) for s in data]

        id = self.valida.solo_numeros("Ingrese el ID de la asignatura a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        asignaturas = [a for a in asignaturas if a.id != int(id)]

        # Convertir los objetos Asignatura de vuelta a diccionarios para guardarlos en el JSON
        data = [asignatura.__dict__ for asignatura in asignaturas]
        self.json_file.save(data)
        print("Asignatura eliminada exitosamente.")
        time.sleep(2)

    def consult(self):
        """Muestra la lista de asignaturas o busca una específica."""
        borrarPantalla()
        gotoxy(0, 2)

        data = self.json_file.read()
        asignaturas = [Asignatura(s['id'], s['descripcion'], s['nivel'], s['active']) for s in data]

        if not asignaturas:
            print("No hay asignaturas registradas.")
            return

        while True:
            print("\n--- Consultar Asignaturas ---")
            print("1. Listar todas las asignaturas")
            print("2. Buscar asignatura por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for asignatura in asignaturas:
                    print(f"ID: {asignatura.id}, Descripción: {asignatura.descripcion}, Nivel: {asignatura.nivel}") 
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID de la asignatura a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                asignatura = next((a for a in asignaturas if a.id == int(id)), None)
                if asignatura:
                    print(f"ID: {asignatura.id}, Descripción: {asignatura.descripcion}, Nivel: {asignatura.nivel}") 
                else:
                    print("Asignatura no encontrada.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")