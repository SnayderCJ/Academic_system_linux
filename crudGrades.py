from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from nota import Nota
from detalleNota import DetalleNota
from estudiante import Estudiante
from periodo import Periodo
from profesor import Profesor
from asignatura import Asignatura
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudGrades(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/grades.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo registro de notas y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        grades_data = self.json_file.read()
        if grades_data:
            id = max([grade['_id'] for grade in grades_data]) + 1
        else:
            id = 1

        # Obtener periodo, profesor y asignatura, asegúrate de validar que existan
        periodos_data = JsonFile(f'{path}/data/periods.json').read()
        profesores_data = JsonFile(f'{path}/data/teachers.json').read()
        asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()

        # Mostrar periodos disponibles (solo los activos)
        borrarPantalla()
        print(f"{cyan_color}\nPeriodos disponibles:{reset_color}")
        for periodo in periodos_data:
            if periodo.get('_active'):
                print(f"ID: {periodo['_id']}, Periodo: {periodo['_periodo']}")

        while True:
            periodo_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del periodo: {reset_color}", f"{red_color}ID de periodo inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
            periodo_seleccionado = next((p for p in periodos_data if p['_id'] == int(periodo_id) and p.get('_active')), None)
            if periodo_seleccionado:
                break
            else:
                print(f"{yellow_color}{' Periodo no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        # Mostrar profesores disponibles (solo los activos)
        borrarPantalla()
        print(f"{cyan_color}\nProfesores disponibles:{reset_color}")
        for profesor in profesores_data:
            if profesor.get('_active'):
                print(f"ID: {profesor['_cedula']}, Nombre: {profesor['_nombre']}")

        while True:
            profesor_cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor: {reset_color}", 0, 5)
            profesor_seleccionado = next((p for p in profesores_data if p['_cedula'] == profesor_cedula and p.get('_active')), None)
            if profesor_seleccionado:
                break
            else:
                print(f"{yellow_color}{' Profesor no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        # Mostrar asignaturas disponibles (solo las activas)
        borrarPantalla()
        print(f"{cyan_color}\nAsignaturas disponibles:{reset_color}")
        for asignatura in asignaturas_data:
            if asignatura.get('_active'):
                print(f"ID: {asignatura['_id']}, Nombre: {asignatura['_descripcion']}")

        while True:
            asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "ID de asignatura inválido. Ingrese un número entero positivo.", 0, 5)
            asignatura_seleccionada = next((a for a in asignaturas_data if a['_id'] == int(asignatura_id) and a.get('_active')), None)
            if asignatura_seleccionada:
                break
            else:
                print(f"{yellow_color}{' Asignatura no encontrado o inactivo. Intente de nuevo. '.center(80)}{reset_color}")

        # Obtener todos los estudiantes desde el archivo students.json
        estudiantes_data = JsonFile(f'{path}/data/students.json').read()

        # Crear la instancia de Nota
         # Crear la instancia de Nota, almacenando solo los IDs
        nueva_nota = Nota(id, 
                        periodo_seleccionado['_periodo'], 
                        profesor_seleccionado['_nombre'],
                        asignatura_seleccionada['_descripcion']
                        )

        for estudiante_data in estudiantes_data:
            if estudiante_data.get('_active'): 
                estudiante = Estudiante(estudiante_data['_cedula'], estudiante_data['_nombre'], estudiante_data['_apellido'], estudiante_data['_fecha_nacimiento'], estudiante_data['_active'])
                while True:
                    try:
                        nota1 = self.valida.solo_decimales(f"Ingrese la primera nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                        nota2 = self.valida.solo_decimales(f"Ingrese la segunda nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                        recuperacion = input(f"Ingrese la nota de recuperación para {estudiante._nombre} (dejar en blanco si no aplica): ")
                        observacion = input(f"Ingrese una observación para {estudiante._nombre} (opcional): ")

                        detalle = DetalleNota(None, estudiante, float(nota1), float(nota2),
                                            float(recuperacion) if recuperacion else None, observacion)
                        nueva_nota.add_detalle_nota(detalle) 
                        break
                    except ValueError as e:
                        print(f"Error: {e}")

        grades_data.append(nueva_nota.__dict__)
        
        for grade in grades_data:
            # Convertir el objeto DetalleNota dentro de _detalleNota a diccionarios
            grade['_detalleNota'] = [detalle.__dict__ for detalle in grade['_detalleNota']]

        self.json_file.save(grades_data)
        print(f"{green_color}{' Registro de calificaciones creado exitosamente. '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un registro de calificaciones existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        grades_data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        grade_dict = next((g for g in grades_data if g['id'] == int(id)), None)

        if grade_dict:
            # Convertir el diccionario a un objeto Nota
            periodo = Periodo(grade_dict['_periodo']['id'], grade_dict['_periodo']['periodo'], grade_dict['_periodo']['active'])
            profesor = Profesor(grade_dict['_profesor']['cedula'], grade_dict['_profesor']['nombre'], grade_dict['_profesor']['active'])
            asignatura = Asignatura(grade_dict['_asignatura']['id'], grade_dict['_asignatura']['descripcion'], grade_dict['_asignatura']['nivel'], grade_dict['_asignatura']['active'])
            detalles_nota = [DetalleNota(None, Estudiante(d['estudiante']['cedula'], d['estudiante']['nombre'], d['estudiante']['apellido'], d['estudiante']['_fecha_nacimiento'], d['estudiante']['_active']), d['nota1'], d['nota2'], d.get('recuperacion'), d.get('observacion')) for d in grade_dict['detalles']]
            grade = Nota(grade_dict['id'], periodo, profesor, asignatura, grade_dict['active'])
            grade._detalleNota = detalles_nota

            # Lógica para obtener nuevos periodo_id, profesor_id y asignatura_id, validando que existan (similar a create())
            periodos_data = JsonFile(f'{path}/data/periods.json').read()
            profesores_data = JsonFile(f'{path}/data/teachers.json').read()
            asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()

            # Mostrar periodos disponibles
            print("\nPeriodos disponibles:")
            for periodo in periodos_data:
                if periodo.get('active'):
                    print(f"ID: {periodo['id']}, Periodo: {periodo['periodo']}")

            while True:
                periodo_id = self.valida.solo_numeros("Ingrese el ID del periodo: ", "ID de periodo inválido. Ingrese un número entero positivo.")
                periodo_seleccionado = next((p for p in periodos_data if p['id'] == int(periodo_id) and p.get('active')), None)
                if periodo_seleccionado:
                    break
                else:
                    print("Periodo no encontrado o inactivo. Intente de nuevo.")

            # Mostrar profesores disponibles
            print("\nProfesores disponibles:")
            for profesor in profesores_data:
                if profesor.get('active'):
                    print(f"ID: {profesor['cedula']}, Nombre: {profesor['nombre']}")

            while True:
                profesor_cedula = self.valida.cedula("Ingrese la cédula del profesor: ", 0, 5)
                profesor_seleccionado = next((p for p in profesores_data if p['cedula'] == profesor_cedula and p.get('active')), None)
                if profesor_seleccionado:
                    break
                else:
                    print("Profesor no encontrado o inactivo. Intente de nuevo.")

            # Mostrar asignaturas disponibles
            print("\nAsignaturas disponibles:")
            for asignatura in asignaturas_data:
                if asignatura.get('active'):
                    print(f"ID: {asignatura['id']}, Nombre: {asignatura['descripcion']}")

            while True:
                asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "ID de asignatura inválido. Ingrese un número entero positivo.")
                asignatura_seleccionada = next((a for a in asignaturas_data if a['id'] == int(asignatura_id) and a.get('active')), None)
                if asignatura_seleccionada:
                    break
                else:
                    print("Asignatura no encontrada o inactiva. Intente de nuevo.")

            # Actualizar los datos del registro de calificaciones
            grade._periodo = Periodo(periodo_seleccionado['id'], periodo_seleccionado['periodo'], periodo_seleccionado.get('active', True))
            grade._profesor = Profesor(profesor_seleccionado['cedula'], profesor_seleccionado['nombre'], profesor_seleccionado.get('active', True))
            grade._asignatura = Asignatura(asignatura_seleccionada['id'], asignatura_seleccionada['descripcion'], asignatura_seleccionada.get('nivel'), asignatura_seleccionada.get('active', True))

            # Lógica para actualizar los detalles de las notas de los estudiantes
            for detalle in grade._detalleNota:
                while True:
                    try:
                        print(f"\nEstudiante: {detalle.estudiante.nombre}")
                        nueva_nota1 = self.valida.solo_decimales(f"Ingrese la nueva primera nota (actual: {detalle.nota1}): ", "Nota inválida. Ingrese un número decimal positivo.")
                        nueva_nota2 = self.valida.solo_decimales(f"Ingrese la nueva segunda nota (actual: {detalle.nota2}): ", "Nota inválida. Ingrese un número decimal positivo.")
                        nueva_recuperacion = input(f"Ingrese la nueva nota de recuperación (actual: {detalle.recuperacion}): ")
                        nueva_observacion = input(f"Ingrese una nueva observación (actual: {detalle.observacion}): ")

                        detalle.nota1 = float(nueva_nota1)
                        detalle.nota2 = float(nueva_nota2)
                        detalle.recuperacion = float(nueva_recuperacion) if nueva_recuperacion else None
                        detalle.observacion = nueva_observacion
                        break
                    except ValueError as e:
                        print(f"Error: {e}")

            # Convertir el objeto Nota de vuelta a un diccionario para guardar los cambios
            grade_dict = grade.__dict__
            # Convertir los objetos DetalleNota dentro de _detalleNota a diccionarios
            grade_dict['_detalleNota'] = [detalle.__dict__ for detalle in grade._detalleNota]
            # Actualizar el diccionario original en grades_data
            for i, g in enumerate(grades_data):
                if g['id'] == grade.id:
                    grades_data[i] = grade_dict
                    break

            self.json_file.save(grades_data)
            print("Registro de calificaciones actualizado exitosamente.")
            time.sleep(2)
        else:
            print("Registro de calificaciones no encontrado.")
            time.sleep(2)

    def delete(self):
        """Elimina un registro de calificaciones del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()

        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        registro_a_eliminar = next((g for g in data if g['id'] == int(id)), None)

        if registro_a_eliminar:
            # Convertir el diccionario a un objeto Nota para acceder a los atributos de forma más clara
            periodo = Periodo(registro_a_eliminar['_periodo']['id'], registro_a_eliminar['_periodo']['periodo'], registro_a_eliminar['_periodo']['active'])
            profesor = Profesor(registro_a_eliminar['_profesor']['cedula'], registro_a_eliminar['_profesor']['nombre'], registro_a_eliminar['_profesor']['active'])
            asignatura = Asignatura(registro_a_eliminar['_asignatura']['id'], registro_a_eliminar['_asignatura']['descripcion'], registro_a_eliminar['_asignatura']['nivel'], registro_a_eliminar['_asignatura']['active'])
            detalles_nota = [DetalleNota(None, Estudiante(d['estudiante']['cedula'], d['estudiante']['nombre'], d['estudiante']['apellido'], d['estudiante']['_fecha_nacimiento'], d['estudiante']['_active']), d['nota1'], d['nota2'], d.get('recuperacion'), d.get('observacion')) for d in registro_a_eliminar['detalles']]
            nota = Nota(registro_a_eliminar['id'], periodo, profesor, asignatura, registro_a_eliminar['active'])
            nota._detalleNota = detalles_nota

            # Mostrar los detalles del registro antes de eliminarlo
            print("\nDetalles del registro a eliminar:")
            print(f"ID: {nota.id}")
            print(f"Periodo: {nota.periodo.periodo}")
            print(f"Profesor: {nota.profesor.nombre}")
            print(f"Asignatura: {nota.asignatura.descripcion}")
            for detalle in nota.detalleNota:
                print(f"  - Estudiante: {detalle.estudiante.nombre} {detalle.estudiante.apellido}, Nota 1: {detalle.nota1}, Nota 2: {detalle.nota2}, Recuperación: {detalle.recuperacion}, Observación: {detalle.observacion}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este registro de notas? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                data = [g for g in data if g['id'] != int(id)]
                self.json_file.save(data)
                print(f"{green_color}{' Registro de notas eliminado exitosamente. '.center(80)}{reset_color}")
            else:
                print(f"{yellow_color}{' Eliminación cancelada. '.center(80)}{reset_color}")
        else:
            print(f"{red_color}{' Registro de notas no encontrado. '.center(80)}{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de registros de calificaciones o busca uno específico."""
        borrarPantalla()
        gotoxy(0, 2)

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
                for grade_dict in data:
                    # Convertir el diccionario a un objeto Nota para acceder a los atributos de forma más clara
                    periodo = Periodo(grade_dict['_periodo']['id'], grade_dict['_periodo']['periodo'], grade_dict['_periodo']['active'])
                    profesor = Profesor(grade_dict['_profesor']['cedula'], grade_dict['_profesor']['nombre'], grade_dict['_profesor']['active'])
                    asignatura = Asignatura(grade_dict['_asignatura']['id'], grade_dict['_asignatura']['descripcion'], grade_dict['_asignatura']['nivel'], grade_dict['_asignatura']['active'])
                    grade = Nota(grade_dict['id'], periodo, profesor, asignatura, grade_dict['active'])

                    print(f"\nID: {grade.id}, Periodo: {grade.periodo.periodo}, Profesor: {grade.profesor.nombre}, Asignatura: {grade.asignatura.descripcion}")
                    for detalle in grade.detalleNota:
                        print(f"  - Estudiante: {detalle.estudiante.nombre} {detalle.estudiante.apellido}, Nota 1: {detalle.nota1}, Nota 2: {detalle.nota2}, Recuperación: {detalle.recuperacion}, Observación: {detalle.observacion}")
            
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del registro a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                grade_dict = next((g for g in data if g['id'] == int(id)), None)
                if grade_dict:
                    periodo = Periodo(grade_dict['_periodo']['id'], grade_dict['_periodo']['periodo'], grade_dict['_periodo']['active'])
                    profesor = Profesor(grade_dict['_profesor']['cedula'], grade_dict['_profesor']['nombre'], grade_dict['_profesor']['active'])
                    asignatura = Asignatura(grade_dict['_asignatura']['id'], grade_dict['_asignatura']['descripcion'], grade_dict['_asignatura']['nivel'], grade_dict['_asignatura']['active'])
                    grade = Nota(grade_dict['id'], periodo, profesor, asignatura, grade_dict['active'])

                    print(f"\nID: {grade.id}, Periodo: {grade.periodo.periodo}, Profesor: {grade.profesor.nombre}, Asignatura: {grade.asignatura.descripcion}")
                    for detalle in grade.detalleNota:
                        print(f"  - Estudiante: {detalle.estudiante.nombre} {detalle.estudiante.apellido}, Nota 1: {detalle.nota1}, Nota 2: {detalle.nota2}, Recuperación: {detalle.recuperacion}, Observación: {detalle.observacion}") 
                else:
                    print("Registro de calificaciones no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")