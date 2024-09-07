from Icrud import Icrud
from clsJson import JsonFile
from components import Valida

class CrudTeacher(Icrud):
    def __init__(self):
        self.json_file = JsonFile('teachers.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo profesor y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        if data:
            id = max([teacher['id'] for teacher in data]) + 1  # Asigna un nuevo ID incremental
        else:
            id = 1

        teacher = {
            'id': id,
            'nombre': self.valida.solo_letras("Ingrese el nombre del profesor: ", "Nombre inválido. Solo se permiten letras."),
            # Puedes agregar más atributos relevantes para un profesor, como:
            # 'especialidad': input("Ingrese la especialidad del profesor: "),
            # 'fecha_contratacion': date.today().strftime('%Y-%m-%d'),  # Fecha actual en formato YYYY-MM-DD
            # 'activo': True  # Puedes manejar el estado de actividad del profesor
        }
        data.append(teacher)
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