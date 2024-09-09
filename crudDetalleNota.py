from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from detalleNota import DetalleNota
from estudiante import Estudiante
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudDetalleNota(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/detalleNota.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo detalle de nota y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Detalle de Nota '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        if data:
            id = max([detalle['id'] for detalle in data]) + 1
        else:
            id = 1

        # Obtener estudiantes disponibles (solo los activos)
        estudiantes_data = JsonFile(f'{path}/data/students.json').read()
        estudiantes = [Estudiante(e['_cedula'], e['_nombre'], e['_apellido'], e['_fecha_nacimiento'], e['_active']) for e in estudiantes_data]
        estudiantes_activos = [estudiante for estudiante in estudiantes if estudiante.active]

        if not estudiantes_activos:
            print(f"{yellow_color}No hay estudiantes activos registrados. Debe crear un estudiante antes de crear un detalle de nota.{reset_color}")
            time.sleep(2)
            return

        print("\nEstudiantes disponibles:")
        for estudiante in estudiantes_activos:
            print(f"ID: {estudiante.cedula}, Nombre: {estudiante.nombre} {estudiante.apellido}")

        # Solicitar al usuario que elija un estudiante válido
        while True:
            cedula_estudiante = self.valida.cedula("Ingrese la cédula del estudiante: ", 0, 5)
            estudiante_seleccionado = next((e for e in estudiantes_activos if e.cedula == cedula_estudiante), None)
            if estudiante_seleccionado:
                break
            else:
                print("Estudiante no encontrado o inactivo. Intente de nuevo.")

        detalle_nota = {
            'id': id,
            'estudiante_id': estudiante_seleccionado.cedula,  # Almacenar la cédula del estudiante
            'nota1': self.valida.solo_decimales("Ingrese la primera nota: ", "Nota inválida. Ingrese un número decimal positivo."),
            'nota2': self.valida.solo_decimales("Ingrese la segunda nota: ", "Nota inválida. Ingrese un número decimal positivo."),
            'recuperacion': self.valida.solo_decimales("Ingrese la nota de recuperación (si aplica): ", "Nota inválida. Ingrese un número decimal positivo o deje en blanco.", opcional=True),
            'observacion': input("Ingrese una observación (opcional): ")
        }

        data.append(detalle_nota)
        self.json_file.save(data)
        print("Detalle de nota creado exitosamente.")
        time.sleep(2)

    def update(self):
        """Actualiza un detalle de nota existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Detalle de Nota '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()

        id = self.valida.solo_numeros("Ingrese el ID del detalle de nota a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        detalle_nota = next((d for d in data if d['id'] == int(id)), None)

        if detalle_nota:
            # Obtener estudiantes disponibles (solo los activos)
            estudiantes_data = JsonFile(f'{path}/data/students.json').read()
            estudiantes = [Estudiante(e['_cedula'], e['_nombre'], e['_apellido'], e['_fecha_nacimiento'], e['_active']) for e in estudiantes_data]
            estudiantes_activos = [estudiante for estudiante in estudiantes if estudiante.active]

            if not estudiantes_activos:
                print(f"{yellow_color}No hay estudiantes activos registrados. No se puede actualizar el estudiante asociado al detalle de nota.{reset_color}")
            else:
                print("\nEstudiantes disponibles:")
                for estudiante in estudiantes_activos:
                    print(f"ID: {estudiante.cedula}, Nombre: {estudiante.nombre} {estudiante.apellido}")

                # Solicitar al usuario que elija un estudiante válido o mantenga el actual
                while True:
                    cedula_estudiante_input = input(f"Ingrese la nueva cédula del estudiante (Enter para mantener '{detalle_nota['estudiante_id']}'): ")
                    if cedula_estudiante_input == "":
                        break  # Mantener el estudiante actual
                    try:
                        cedula_estudiante = self.valida.cedula(cedula_estudiante_input, 0, 0)  # Validar la cédula
                        if cedula_estudiante is not None:
                            estudiante_seleccionado = next((e for e in estudiantes_activos if e.cedula == cedula_estudiante), None)
                            if estudiante_seleccionado:
                                detalle_nota['estudiante_id'] = estudiante_seleccionado.cedula
                                break
                            else:
                                print("Estudiante no encontrado o inactivo. Intente de nuevo.")
                    except ValueError:
                        print("Cédula inválida. Ingrese una cédula válida o presione Enter para mantener el estudiante actual.")

            # Solicitar nuevas notas, manteniendo las originales si se presiona Enter
            while True:
                nueva_nota1_input = input(f"Ingrese la nueva primera nota (Enter para mantener {detalle_nota['nota1']}): ")
                if nueva_nota1_input == "":
                    break
                try:
                    nueva_nota1 = float(nueva_nota1_input)
                    if nueva_nota1 >= 0:  # Asumimos que las notas pueden ser 0
                        detalle_nota['nota1'] = nueva_nota1
                        break
                    else:
                        print(f"{red_color}Nota inválida. Ingrese un número decimal positivo o 0, o Enter para mantener la nota actual.{reset_color}")
                except ValueError:
                    print(f"{red_color}Nota inválida. Ingrese un número decimal positivo o 0, o Enter para mantener la nota actual.{reset_color}")

            # ... (Lógica similar para actualizar nota2, recuperacion y observacion)

            self.json_file.save(data)
            print("Detalle de nota actualizado exitosamente.")
            time.sleep(2)
        else:
            print("Detalle de nota no encontrado.")
            time.sleep(2)

    def delete(self):
        """Elimina un detalle de nota del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Detalle de Nota '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()

        id = self.valida.solo_numeros("Ingrese el ID del detalle de nota a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        data = [d for d in data if d['id'] != int(id)]

        self.json_file.save(data)
        print("Detalle de nota eliminado exitosamente.")
        time.sleep(2)

    def consult(self):
        """Muestra la lista de detalles de notas o busca uno específico."""
        borrarPantalla()
        gotoxy(0, 2)

        data = self.json_file.read()

        if not data:
            print("No hay detalles de notas registrados.")
            return

        while True:
            print("\n--- Consultar Detalles de Notas ---")
            print("1. Listar todos los detalles de notas")
            print("2. Buscar detalle de nota por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                borrarPantalla()
                for detalle in data:
                    # Obtener el nombre del estudiante asociado al detalle de nota
                    estudiantes_data = JsonFile(f'{path}/data/students.json').read()
                    estudiante = next((e for e in estudiantes_data if e['cedula'] == detalle['estudiante_id']), None)
                    nombre_estudiante = estudiante['nombre'] if estudiante else "Estudiante no encontrado"

                    print(f"ID: {detalle['id']}, Estudiante: {nombre_estudiante}, Nota 1: {detalle['nota1']}, Nota 2: {detalle['nota2']}, Recuperación: {detalle['recuperacion']}, Observación: {detalle['observacion']}")
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros("Ingrese el ID del detalle de nota a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                detalle = next((d for d in data if d['id'] == int(id)), None)
                if detalle:
                    # Obtener el nombre del estudiante asociado al detalle de nota
                    estudiantes_data = JsonFile(f'{path}/data/students.json').read()
                    estudiante = next((e for e in estudiantes_data if e['cedula'] == detalle['estudiante_id']), None)
                    nombre_estudiante = estudiante['nombre'] if estudiante else "Estudiante no encontrado"

                    print(f"ID: {detalle['id']}, Estudiante: {nombre_estudiante}, Nota 1: {detalle['nota1']}, Nota 2: {detalle['nota2']}, Recuperación: {detalle['recuperacion']}, Observación: {detalle['observacion']}")
                else:
                    print("Detalle de nota no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")