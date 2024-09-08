from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from profesor import Profesor
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color
import time

class CrudTeacher(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/teachers.json")
        self.valida = Valida()

    def create(self):
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Profesor '.center(80)}{reset_color}")
        linea(80, green_color)
        """Crea un nuevo profesor y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        # Convertir los datos del JSON a objetos Profesor
        profesores = [Profesor(t['cedula'], t['nombre'], t.get('active', True)) for t in data]

        while True:  # Bucle para asegurar que la cédula sea única y válida
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor: {reset_color}", 0, 5)
            if cedula is None:  # Manejar el caso de error en la validación
                continue
            if not any(p.cedula == cedula for p in profesores):
                break
            else:
                print(f"{red_color}Cédula ya registrada. Intente de nuevo.{reset_color}")

        nombre = self.valida.solo_letras("Ingrese el nombre del profesor: ", "Nombre inválido. Solo se permiten letras.")
        # ... (solicitar otros atributos del profesor si es necesario)

        nuevo_profesor = Profesor(cedula, nombre, True) 
        profesores.append(nuevo_profesor)

        # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
        data = [profesor.__dict__ for profesor in profesores]
        self.json_file.save(data)
        print("Profesor creado exitosamente.")

    def update(self):
        """Actualiza un profesor existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Profesor '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        profesores = [Profesor(t['cedula'], t['nombre'], t.get('active', True)) for t in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a actualizar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        profesor = next((p for p in profesores if p.cedula == cedula), None)

        if profesor:
            profesor.nombre = self.valida.solo_letras("Ingrese el nuevo nombre del profesor: ", "Nombre inválido. Solo se permiten letras.")
            # Actualiza otros atributos del profesor según sea necesario, utilizando profesor.atributo = nuevo_valor

            # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
            data = [profesor.__dict__ for profesor in profesores]
            self.json_file.save(data)
            print("Profesor actualizado exitosamente.")
        else:
            print("Profesor no encontrado.")

    def delete(self):
        """Elimina un profesor del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Profesor '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        profesores = [Profesor(t['cedula'], t['nombre'], t.get('active', True)) for t in data]

        while True:
            cedula = self.valida.cedula("Ingrese la cédula del profesor a eliminar: ", 0, 5)
            if cedula is not None:
                break

        profesores = [p for p in profesores if p.cedula != cedula]

        # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
        data = [profesor.__dict__ for profesor in profesores]
        self.json_file.save(data)
        print("Profesor eliminado exitosamente.")

    def consult(self):
        """Muestra la lista de profesores o busca uno específico."""
        borrarPantalla()
        gotoxy(0, 2)

        data = self.json_file.read()
        profesores = [Profesor(t['cedula'], t['nombre'], t.get('active', True)) for t in data]

        if not profesores:
            print("No hay profesores registrados.")
            return

        while True:
            print("\n--- Consultar Profesores ---")
            print("1. Listar todos los profesores")
            print("2. Buscar profesor por cédula") 
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for profesor in profesores:
                    print(f"Cédula: {profesor.cedula}, Nombre: {profesor.nombre}")  # Muestra otros atributos según sea necesario
            elif opcion == '2':
                while True:
                    cedula = self.valida.cedula("Ingrese la cédula del profesor a buscar: ", 0, 5)
                    if cedula is not None:
                        break

                profesor = next((p for p in profesores if p.cedula == cedula), None)
                if profesor:
                    print(f"Cédula: {profesor.cedula}, Nombre: {profesor.nombre}")  # Muestra otros atributos según sea necesario
                else:
                    print("Profesor no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")