from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from periodo import Periodo
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudPeriodo(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/periodos.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo periodo académico y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Periodo Académico '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        # Convertir los datos del JSON a objetos Periodo
        periodos = [Periodo(p['id'], p['periodo'], p.get('active', True)) for p in data]

        if periodos:
            id = max([periodo.id for periodo in periodos]) + 1
        else:
            id = 1

        nombre_periodo = input("Ingrese el nombre del periodo académico: ")
        while not nombre_periodo:
            print(f"{red_color}El nombre del periodo no puede estar vacío. Intente de nuevo.{reset_color}")
            nombre_periodo = input("Ingrese el nombre del periodo académico: ")

        nuevo_periodo = Periodo(id, nombre_periodo, True)
        periodos.append(nuevo_periodo)

        # Convertir los objetos Periodo de vuelta a diccionarios para guardarlos en el JSON
        data = [periodo.__dict__ for periodo in periodos]
        self.json_file.save(data)
        print("Periodo académico creado exitosamente.")
        time.sleep(2)

    def update(self):
        """Actualiza un periodo académico existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Periodo Académico '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        periodos = [Periodo(p['id'], p['periodo'], p.get('active', True)) for p in data]

        id = self.valida.solo_numeros("Ingrese el ID del periodo académico a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        periodo = next((p for p in periodos if p.id == int(id)), None)

        if periodo:
            nuevo_nombre = input(f"Ingrese el nuevo nombre del periodo académico (actual: {periodo.periodo}): ")
            if nuevo_nombre:
                periodo.periodo = nuevo_nombre

            while True:
                nuevo_estado = input(f"Ingrese el nuevo estado del periodo (activo/inactivo) (actual: {'activo' if periodo.active else 'inactivo'}): ")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    periodo.active = (nuevo_estado.lower() == 'activo')
                    break
                else:
                    print("Estado inválido. Ingrese 'activo' o 'inactivo'.")

            # Convertir los objetos Periodo de vuelta a diccionarios para guardarlos en el JSON
            data = [periodo.__dict__ for periodo in periodos]
            self.json_file.save(data)
            print("Periodo académico actualizado exitosamente.")
            time.sleep(2)
        else:
            print("Periodo académico no encontrado.")
            time.sleep(2)

    def delete(self):
        """Elimina un periodo académico del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Periodo Académico '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        periodos = [Periodo(p['id'], p['periodo'], p.get('active', True)) for p in data]

        id = self.valida.solo_numeros("Ingrese el ID del periodo académico a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        periodos = [p for p in periodos if p.id != int(id)]

        # Convertir los objetos Periodo de vuelta a diccionarios para guardarlos en el JSON
        data = [periodo.__dict__ for periodo in periodos]
        self.json_file.save(data)
        print("Periodo académico eliminado exitosamente.")
        time.sleep(2)

    def consult(self):
        """Muestra la lista de periodos académicos o busca uno específico."""
        borrarPantalla()
        gotoxy(0, 2)

        data = self.json_file.read()
        periodos = [Periodo(p['id'], p['periodo'], p.get('active', True)) for p in data]

        if not periodos:
            print("No hay periodos académicos registrados.")
            return

        while True:
            print("\n--- Consultar Periodos Académicos ---")
            print("1. Listar todos los periodos académicos")
            print("2. Buscar periodo académico por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for periodo in periodos:
                    print(f"ID: {periodo.id}, Periodo: {periodo.periodo}, Estado: {'Activo' if periodo.active else 'Inactivo'}")
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del periodo académico a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                periodo = next((p for p in periodos if p.id == int(id)), None)
                if periodo:
                    print(f"ID: {periodo.id}, Periodo: {periodo.periodo}, Estado: {'Activo' if periodo.active else 'Inactivo'}")
                else:
                    print("Periodo académico no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")