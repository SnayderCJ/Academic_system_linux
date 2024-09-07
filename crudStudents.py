from Icrud import Icrud
from clsJson import JsonFile
from components import Valida

class CrudStudents(Icrud):
    def __init__(self):
        self.json_file = JsonFile('students.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo estudiante y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        if data:
            id = max([student['id'] for student in data]) + 1  # Asigna un nuevo ID incremental
        else:
            id = 1

        student = {
            'id': id,
            'nombre': self.valida.solo_letras("Ingrese el nombre del estudiante: ", "Nombre inválido. Solo se permiten letras."),
            'edad': self.valida.solo_numeros("Ingrese la edad del estudiante: ", "Edad inválida. Ingrese un número entero positivo."),
            'grado': self.valida.solo_letras("Ingrese el grado del estudiante: ", "Grado inválido. Solo se permiten letras."),
            'escuela': input("Ingrese la escuela del estudiante: "),
            'promedio': self.valida.solo_decimales("Ingrese el promedio del estudiante: ", "Promedio inválido. Ingrese un número decimal positivo.")
        }
        
        data.append(student)
        self.json_file.save(data)
        print("Estudiante creado exitosamente.")

    def update(self):
        """Actualiza un estudiante existente en el archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del estudiante a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        student = next((s for s in data if s['id'] == int(id)), None)
        if student:
            student['nombre'] = self.valida.solo_letras("Ingrese el nuevo nombre del estudiante: ", "Nombre inválido. Solo se permiten letras.")
            student['edad'] = self.valida.solo_numeros("Ingrese la nueva edad del estudiante: ", "Edad inválida. Ingrese un número entero positivo.")
            student['grado'] = self.valida.solo_letras("Ingrese el nuevo grado del estudiante: ", "Grado inválido. Solo se permiten letras.")
            student['escuela'] = input("Ingrese la nueva escuela del estudiante: ")
            student['promedio'] = self.valida.solo_decimales("Ingrese el nuevo promedio del estudiante: ", "Promedio inválido. Ingrese un número decimal positivo.")
            self.json_file.save(data)
            print("Estudiante actualizado exitosamente.")
        else:
            print("Estudiante no encontrado.")

    def delete(self):
        """Elimina un estudiante del archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del estudiante a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        data = [s for s in data if s['id'] != int(id)]
        self.json_file.save(data)
        print("Estudiante eliminado exitosamente.")

    def consult(self):
        """Muestra la lista de estudiantes o busca uno específico."""
        data = self.json_file.read()
        if not data:
            print("No hay estudiantes registrados.")
            return

        while True:
            print("\n--- Consultar Estudiantes ---")
            print("1. Listar todos los estudiantes")
            print("2. Buscar estudiante por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for student in data:
                    print(f"ID: {student['id']}, Nombre: {student['nombre']}, Edad: {student['edad']}, Grado: {student['grado']}, Escuela: {student['escuela']}, Promedio: {student['promedio']}")
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del estudiante a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                student = next((s for s in data if s['id'] == int(id)), None)
                if student:
                    print(f"ID: {student['id']}, Nombre: {student['nombre']}, Edad: {student['edad']}, Grado: {student['grado']}, Escuela: {student['escuela']}, Promedio: {student['promedio']}")
                else:
                    print("Estudiante no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")