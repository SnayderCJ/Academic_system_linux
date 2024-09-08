from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from profesor import Profesor
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color

class CrudTeacher(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/teachers.json")
        self.valida = Valida()

    def create(self):
        """Crea un nuevo profesor y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        # Convertir los datos del JSON a objetos Profesor
        profesores = [Profesor(t['id'], t['nombre'], t.get('active', True)) for t in data]

        if profesores:
            id = max([teacher.id for teacher in profesores]) + 1
        else:
            id = 1

        nombre = self.valida.solo_letras("Ingrese el nombre del profesor: ", "Nombre inválido. Solo se permiten letras.")

        nuevo_profesor = Profesor(id, nombre, True)  # Crear un objeto Profesor
        profesores.append(nuevo_profesor)

        # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
        data = [profesor.__dict__ for profesor in profesores]
        self.json_file.save(data)
        print("Profesor creado exitosamente.")

    def update(self):
        """Actualiza un profesor existente en el archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del profesor a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        teacher = next((t for t in data if t['id'] == int(id)), None)
        if teacher:
            teacher['nombre'] = self.valida.solo_letras("Ingrese el nuevo nombre del profesor: ", "Nombre inválido. Solo se permiten letras.")
            # Actualiza otros atributos del profesor según sea necesario
            self.json_file.save(data)
            print("Profesor actualizado exitosamente.")
        else:
            print("Profesor no encontrado.")

    def delete(self):
        """Elimina un profesor del archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del profesor a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        data = [t for t in data if t['id'] != int(id)]
        self.json_file.save(data)
        print("Profesor eliminado exitosamente.")

    def consult(self):
        """Muestra la lista de profesores o busca uno específico."""
        data = self.json_file.read()
        if not data:
            print("No hay profesores registrados.")
            return

        while True:
            print("\n--- Consultar Profesores ---")
            print("1. Listar todos los profesores")
            print("2. Buscar profesor por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for teacher in data:
                    print(f"ID: {teacher['id']}, Nombre: {teacher['nombre']}")  # Muestra otros atributos según sea necesario
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del profesor a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                teacher = next((t for t in data if t['id'] == int(id)), None)
                if teacher:
                    print(f"ID: {teacher['id']}, Nombre: {teacher['nombre']}")  # Muestra otros atributos según sea necesario
                else:
                    print("Profesor no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")