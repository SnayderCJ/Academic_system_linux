from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color
from paths import path
import time

class CrudStudents(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/students.json") # Modifica la ruta del archivo JSON
        self.valida = Valida()

    def create(self):
        """Crea un nuevo estudiante y lo guarda en el archivo JSON."""
        borrarPantalla()  # Limpia la pantalla antes de mostrar el formulario de creación
        linea(80,green_color)
        print(f"{purple_color}{' Crear Estudiante '.center(80)}{reset_color}")
        linea(80,green_color)

        data = self.json_file.read()

        while True:  
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante: {reset_color}", 0, 5)
            if not any(s['cedula'] == cedula for s in data):  # Verificar si la cédula ya existe
                break
            else:
                print(f"{red_color}Cédula ya registrada. Intente de nuevo.{reset_color}")
        
        student = {
            'cedula': cedula,
            'nombre': self.valida.solo_letras(f"{purple_color}Ingrese el nombre del estudiante: {reset_color}", f"{red_color} Nombre inválido. Solo se permiten letras.{reset_color}"),
            'apellido': self.valida.solo_letras(f"{purple_color}Ingrese el apellido del estudiante: {reset_color}", f"{red_color} Apellido inválido. Solo se permiten letras.{reset_color}"),
            'edad': self.valida.solo_numeros(f'{purple_color}Ingrese la edad del estudiante: {reset_color}', f"{red_color}Edad inválida. Ingrese un número entero positivo. {reset_color}", 0, 7),  # Utiliza gotoxy aquí si es necesario
            'grado': self.valida.solo_letras(f"{purple_color}Ingrese el grado del estudiante: {reset_color}", f"{red_color}Grado inválido. Solo se permiten letras.{reset_color}"),
            'escuela': input(f"          ------>   | {purple_color}Ingrese la escuela del estudiante: {reset_color}"),
            'promedio': self.valida.solo_decimales(f"{purple_color}Ingrese el promedio del estudiante: {reset_color}", f"{red_color}Promedio inválido. Ingrese un número decimal positivo.{reset_color}")
        }

        data.append(student)
        self.json_file.save(data)
        print(f"{green_color}{' Estudiante Creado Exitosamente... '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un estudiante existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Estudiante '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()

        while True:  # Bucle para asegurar que se ingrese una cédula válida
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a actualizar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        student = next((s for s in data if s['cedula'] == cedula), None)
        if student:
            # Solicitar nuevo nombre, manteniendo el original si se presiona Enter
            nuevo_nombre = input(f"          ------>   | {purple_color}Ingrese el nuevo nombre del estudiante (Enter para mantener {student['nombre']}): {reset_color}")
            student['nombre'] = nuevo_nombre if nuevo_nombre else student['nombre']

            # Solicitar nuevo apellido, manteniendo el original si se presiona Enter
            nuevo_apellido = input(f"          ------>   | {purple_color}Ingrese el nuevo apellido del estudiante (Enter para mantener {student['apellido']}): {reset_color}")
            student['apellido'] = nuevo_apellido if nuevo_apellido else student['apellido']

            # Solicitar nueva edad, manteniendo la original si se presiona Enter
            while True:
                nueva_edad_input = input(f"          ------>   | {purple_color}Ingrese la nueva edad del estudiante (Enter para mantener {student['edad']}): {reset_color}")
                if nueva_edad_input == "":
                    break  # Mantener la edad original
                try:
                    nueva_edad = int(nueva_edad_input)
                    if nueva_edad > 0:
                        student['edad'] = nueva_edad
                        break
                    else:
                        print(f"{red_color}Edad inválida. Ingrese un número entero positivo o Enter para mantener la edad actual.{reset_color}")
                except ValueError:
                    print(f"{red_color}Edad inválida. Ingrese un número entero positivo o Enter para mantener la edad actual.{reset_color}")

            # Solicitar nuevo grado, manteniendo el original si se presiona Enter
            nuevo_grado = input(f"          ------>   | {purple_color}Ingrese el nuevo grado del estudiante (Enter para mantener {student['grado']}): {reset_color}")
            student['grado'] = nuevo_grado if nuevo_grado else student['grado']

            # Solicitar nueva escuela, manteniendo la original si se presiona Enter
            nueva_escuela = input(f"          ------>   | {purple_color}Ingrese la nueva escuela del estudiante (Enter para mantener {student['escuela']}): {reset_color}")
            student['escuela'] = nueva_escuela if nueva_escuela else student['escuela']

            # Solicitar nuevo promedio, manteniendo el original si se presiona Enter
            while True:
                nuevo_promedio_input = input(f"          ------>   | {purple_color}Ingrese el nuevo promedio del estudiante (Enter para mantener {student['promedio']}): {reset_color}")
                if nuevo_promedio_input == "":
                    break
                try:
                    nuevo_promedio = float(nuevo_promedio_input)
                    if nuevo_promedio > 0:
                        student['promedio'] = nuevo_promedio
                        break
                    else:
                        print(f"{red_color}Promedio inválido. Ingrese un número decimal positivo o Enter para mantener el promedio actual.{reset_color}")
                except ValueError:
                    print(f"{red_color}Promedio inválido. Ingrese un número decimal positivo o Enter para mantener el promedio actual.{reset_color}")

            self.json_file.save(data)
            print()
            print(f"{green_color}{' Estudiante actualizado exitosamente... '.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print(f"{red_color}{' Estudiante no encontrado. '.center(80)}{reset_color}")
            time.sleep(2)


    def delete(self):
        borrarPantalla()
        linea(80,green_color)
        print(f"{purple_color}{' Eliminar Estudiante '.center(80)}{reset_color}")
        linea(80,green_color)

        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese la cedula del estudiante a eliminar: ", "Cedula inválido. Ingrese un número entero positivo.", 0, 5)
        data = [s for s in data if s['cedula'] != int(id)]
        self.json_file.save(data)
        print(f"{green_color}{' Estudiante eliminado exitosamente.... '.center(80)}{reset_color}")

    def consult(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Estudiante(s) '.center(80)}{reset_color}")
        linea(80, green_color)
        
        """Muestra la lista de estudiantes o busca uno específico."""
        data = self.json_file.read()
        if not data:
            print(f"{yellow_color}{' No hay estudiantes registrados. '.center(80)}{reset_color}")
            time.sleep(2)
            return

        while True:
            print("1. Listar todos los estudiantes")
            print("2. Buscar estudiante por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                borrarPantalla()
                for student in data:
                    print(f"Cedula: {student['cedula']}, Nombre: {student['nombre']}, Edad: {student['edad']}, Grado: {student['grado']}, Escuela: {student['escuela']}, Promedio: {student['promedio']}")
            elif opcion == '2':
                borrarPantalla()
                cedula = self.valida.cedula(f"{purple_color}Ingrese el ID del estudiante a buscar: {reset_color}", 0, 5)
                student = next((s for s in data if s['cedula'] == cedula), None)
                if student:
                    print(f"Cedula: {student['cedula']}, Nombre: {student['nombre']}, Edad: {student['edad']}, Grado: {student['grado']}, Escuela: {student['escuela']}, Promedio: {student['promedio']}")
                else:
                    print("Estudiante no encontrado.")
            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo. '.center(80)}{reset_color}")
                time.sleep(2)