from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from nota import Nota
from detalleNota import DetalleNota
from estudiante import Estudiante

class CrudGrades(Icrud):
    def __init__(self):
        self.json_file = JsonFile('grades.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo registro de calificaciones y lo guarda en el archivo JSON."""
        grades_data = self.json_file.read()
        if grades_data:
            id = max([grade['id'] for grade in grades_data]) + 1  # Asigna un nuevo ID incremental
        else:
            id = 1

        # Lógica para obtener periodo, profesor y asignatura, asegúrate de validar que existan
        periodos_data = JsonFile('').read()
        profesores_data = JsonFile('teachers.json').read()
        asignaturas_data = JsonFile('courses.json').read()

        # Mostrar periodos disponibles
        print("\nPeriodos disponibles:")
        for periodo in periodos_data:
            if periodo['active']:  # Solo mostrar periodos activos
                print(f"ID: {periodo['id']}, Periodo: {periodo['periodo']}")

        # Solicitar al usuario que elija un periodo válido
        while True:
            periodo_id = self.valida.solo_numeros("Ingrese el ID del periodo: ", "ID de periodo inválido. Ingrese un número entero positivo.")
            if any(p['id'] == int(periodo_id) and p['active'] for p in periodos_data):
                break
            else:
                print("Periodo no encontrado o inactivo. Intente de nuevo.")

        # Mostrar profesores disponibles
        print("\nProfesores disponibles:")
        for profesor in profesores_data:
            if profesor['active']:
                print(f"ID: {profesor['id']}, Nombre: {profesor['nombre']}")

        # Solicitar al usuario que elija un profesor válido
        while True:
            profesor_id = self.valida.solo_numeros("Ingrese el ID del profesor: ", "ID de profesor inválido. Ingrese un número entero positivo.")
            if any(p['id'] == int(profesor_id) and p['active'] for p in profesores_data):
                break
            else:
                print("Profesor no encontrado o inactivo. Intente de nuevo.")

        # Mostrar asignaturas disponibles
        print("\nAsignaturas disponibles:")
        for asignatura in asignaturas_data:
            if asignatura['active']:
                print(f"ID: {asignatura['id']}, Nombre: {asignatura['descripcion']}")

        # Solicitar al usuario que elija una asignatura válida
        while True:
            asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "ID de asignatura inválido. Ingrese un número entero positivo.")
            if any(a['id'] == int(asignatura_id) and a['active'] for a in asignaturas_data):
                break
            else:
                print("Asignatura no encontrada o inactiva. Intente de nuevo.")

        grade = {
            'id': id,
            'periodo_id': int(periodo_id),
            'profesor_id': int(profesor_id),
            'asignatura_id': int(asignatura_id),
            'detalles': []
        }

        # Lógica para obtener la lista de estudiantes matriculados en la asignatura (PENDIENTE)
        # ... (Aquí debes implementar la lógica para obtener los estudiantes matriculados en la asignatura seleccionada)
        estudiantes_matriculados = []  # Reemplaza con la lógica real

        for estudiante_data in estudiantes_matriculados:
            estudiante = Estudiante(estudiante_data['id'], estudiante_data['nombre'], estudiante_data['active'])
            while True:
                try:
                    nota1 = self.valida.solo_decimales(f"Ingrese la primera nota para {estudiante.nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                    nota2 = self.valida.solo_decimales(f"Ingrese la segunda nota para {estudiante.nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                    recuperacion = input(f"Ingrese la nota de recuperación para {estudiante.nombre} (dejar en blanco si no aplica): ")
                    observacion = input(f"Ingrese una observación para {estudiante.nombre} (opcional): ")

                    detalle = DetalleNota(None, estudiante, float(nota1), float(nota2),
                                          float(recuperacion) if recuperacion else None, observacion)
                    grade['detalles'].append(detalle.__dict__)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

        grades_data.append(grade)
        self.json_file.save(grades_data)
        print("Registro de calificaciones creado exitosamente.")

    def update(self):
        """Actualiza un registro de calificaciones existente en el archivo JSON."""
        grades_data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        grade = next((g for g in grades_data if g['id'] == int(id)), None)

        if grade:
            # Lógica para obtener nuevos periodo_id, profesor_id y asignatura_id, validando que existan (similar a create())
            # ... (Puedes reutilizar el código de la sección correspondiente en el método create)

            # Lógica para actualizar los detalles de las notas de los estudiantes
            for detalle in grade['detalles']:
                estudiante = Estudiante(detalle['estudiante']['id'], detalle['estudiante']['nombre'], detalle['estudiante']['active'])
                while True:
                    try:
                        print(f"\nEstudiante: {estudiante.nombre}")
                        nueva_nota1 = self.valida.solo_decimales(f"Ingrese la nueva primera nota (actual: {detalle['nota1']}): ", "Nota inválida. Ingrese un número decimal positivo.")
                        nueva_nota2 = self.valida.solo_decimales(f"Ingrese la nueva segunda nota (actual: {detalle['nota2']}): ", "Nota inválida. Ingrese un número decimal positivo.")
                        nueva_recuperacion = input(f"Ingrese la nueva nota de recuperación (actual: {detalle['recuperacion']}): ")
                        nueva_observacion = input(f"Ingrese una nueva observación (actual: {detalle['observacion']}): ")

                        detalle['nota1'] = float(nueva_nota1)
                        detalle['nota2'] = float(nueva_nota2)
                        detalle['recuperacion'] = float(nueva_recuperacion) if nueva_recuperacion else None
                        detalle['observacion'] = nueva_observacion
                        break
                    except ValueError as e:
                        print(f"Error: {e}")

            self.json_file.save(grades_data)
            print("Registro de calificaciones actualizado exitosamente.")
        else:
            print("Registro de calificaciones no encontrado.")

    def delete(self):
        """Elimina un registro de calificaciones del archivo JSON."""
        data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        data = [g for g in data if g['id'] != int(id)]
        self.json_file.save(data)
        print("Registro de calificaciones eliminado exitosamente.")

    def consult(self):
        """Muestra la lista de registros de calificaciones o busca uno específico."""
        data = self.json_file.read()
        if not data:
            print("No hay registros de calificaciones.")
            return

        while True:
            print("\n--- Consultar Calificaciones ---")
            print("1. Listar todos los registros de calificaciones")
            print("2. Buscar registro por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for grade in data:
                    print(f"ID: {grade['id']}, Periodo ID: {grade['periodo_id']}, Profesor ID: {grade['profesor_id']}, Asignatura ID: {grade['asignatura_id']}")
                    for detalle in grade['detalles']:
                        estudiante = Estudiante(detalle['estudiante']['id'], detalle['estudiante']['nombre'], detalle['estudiante']['active'])
                        print(f"  - Estudiante: {estudiante.nombre}, Nota 1: {detalle['nota1']}, Nota 2: {detalle['nota2']}, Recuperación: {detalle['recuperacion']}, Observación: {detalle['observacion']}")
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del registro a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                grade = next((g for g in data if g['id'] == int(id)), None)
                if grade:
                    print(f"ID: {grade['id']}, Periodo ID: {grade['periodo_id']}, Profesor ID: {grade['profesor_id']}, Asignatura ID: {grade['asignatura_id']}")
                    for detalle in grade['detalles']:
                        estudiante = Estudiante(detalle['estudiante']['id'], detalle['estudiante']['nombre'], detalle['estudiante']['active'])
                        print(f"  - Estudiante: {estudiante.nombre}, Nota 1: {detalle['nota1']}, Nota 2: {detalle['nota2']}, Recuperación: {detalle['recuperacion']}, Observación: {detalle['observacion']}") 
                else:
                    print("Registro de calificaciones no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")