from Icrud import Icrud
from clsJson import JsonFile
from components import Valida

class CrudCourses(Icrud):
    def __init__(self):
        self.json_file = JsonFile('courses.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo curso y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        if data:
            id = max([course['id'] for course in data]) + 1  # Asigna un nuevo ID incremental
        else:
            id = 1

        course = {
            'id': id,
            'nombre': self.valida.solo_letras("Ingrese el nombre del curso: ", "Nombre inválido. Solo se permiten letras."),
            # Puedes agregar más atributos relevantes para un curso, como:
            # 'descripcion': input("Ingrese la descripción del curso: "),
            # 'creditos': self.valida.solo_numeros("Ingrese el número de créditos del curso: ", "Número de créditos inválido. Ingrese un número entero positivo."),
            # 'profesor_id': self.valida.solo_numeros("Ingrese el ID del profesor asignado al curso: ", "ID de profesor inválido. Ingrese un número entero positivo."),
            # 'activo': True  # Puedes manejar el estado de actividad del curso
        }
        data.append(course)
        self.json_file.save(data)
        print("Curso creado exitosamente.")

    def update(self):
        """Actualiza un curso existente en el archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del curso a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        course = next((c for c in data if c['id'] == int(id)), None)
        if course:
            course['nombre'] = self.valida.solo_letras("Ingrese el nuevo nombre del curso: ", "Nombre inválido. Solo se permiten letras.")
            # Actualiza otros atributos del curso según sea necesario
            self.json_file.save(data)
            print("Curso actualizado exitosamente.")
        else:
            print("Curso no encontrado.")

    def delete(self):
        """Elimina un curso del archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del curso a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        data = [c for c in data if c['id'] != int(id)]
        self.json_file.save(data)
        print("Curso eliminado exitosamente.")

    def consult(self):
        """Muestra la lista de cursos o busca uno específico."""
        data = self.json_file.read()
        if not data:
            print("No hay cursos registrados.")
            return

        while True:
            print("\n--- Consultar Cursos ---")
            print("1. Listar todos los cursos")
            print("2. Buscar curso por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for course in data:
                    print(f"ID: {course['id']}, Nombre: {course['nombre']}")  # Muestra otros atributos según sea necesario
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del curso a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                course = next((c for c in data if c['id'] == int(id)), None)
                if course:
                    print(f"ID: {course['id']}, Nombre: {course['nombre']}")  # Muestra otros atributos según sea necesario
                else:
                    print("Curso no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")