from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from nivel import Nivel
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time

class CrudLevel(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/levels.json')
        self.valida = Valida()

        self.niveles_predefinidos = [
            "Primero de Secundaria",
            "Segundo de Secundaria",
            "Tercero de Secundaria",
            "Cuarto de Secundaria",
            "Quinto de Secundaria",
            "Sexto de Secundaria"
        ]

    def create(self):
        """Crea un nuevo nivel educativo y lo guarda en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Crear Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        # Convertir los datos del JSON a objetos Nivel
        niveles = [Nivel(n['id'], n['nivel']) for n in data]

        if niveles:
            id = max([nivel.id for nivel in niveles]) + 1
        else:
            id = 1

         # Mostrar niveles predefinidos
        print(f"\n{purple_color}Niveles educativos predefinidos:{reset_color}")
        for i, nivel_predefinido in enumerate(self.niveles_predefinidos):
            print(f"{cyan_color}{i+1}. {nivel_predefinido} {reset_color}")

        # Solicitar al usuario que elija un nivel predefinido
        while True:
            opcion = self.valida.solo_numeros("Seleccione el número del nivel educativo: ", 
                                              "Opción inválida. Ingrese un número entero positivo.", 0, 5)
            if 1 <= int(opcion) <= len(self.niveles_predefinidos):
                nombre_nivel = self.niveles_predefinidos[int(opcion) - 1]
                break
            else:
                print("Opción fuera de rango. Intente de nuevo.")

        nuevo_nivel = Nivel(id, nombre_nivel)
        niveles.append(nuevo_nivel)

        # Convertir los objetos Nivel de vuelta a diccionarios para guardarlos en el JSON
        data = [nivel.__dict__ for nivel in niveles]
        self.json_file.save(data)
        print(f"{green_color}{' Nivel educativo creado exitosamente. '.center(80)}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un nivel educativo existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['id'], n['nivel']) for n in data]

        id = self.valida.solo_numeros("Ingrese el ID del nivel educativo a actualizar: ", "ID inválido. Ingrese un número entero positivo.")
        nivel = next((n for n in niveles if n.id == int(id)), None)

        if nivel:
            nivel.nivel = self.valida.solo_letras("Ingrese el nuevo nombre del nivel educativo: ", "Nombre inválido. Solo se permiten letras.")

            while True:
                nuevo_estado = input(f"Ingrese el nuevo estado del nivel (activo/inactivo) (actual: {'activo' if nivel.active else 'inactivo'}): ")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        nivel.activar() 
                    else:
                        nivel.desactivar() 
                    break
                else:
                    print("Estado inválido. Ingrese 'activo' o 'inactivo'.")

            # Convertir los objetos Nivel de vuelta a diccionarios para guardarlos en el JSON
            data = [nivel.__dict__ for nivel in niveles]
            self.json_file.save(data)
            print("Nivel educativo actualizado exitosamente.")
            time.sleep(2)
        else:
            print("Nivel educativo no encontrado.")
            time.sleep(2)

    def delete(self):
        """Elimina un nivel educativo del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['id'], n['nivel']) for n in data]

        id = self.valida.solo_numeros("Ingrese el ID del nivel educativo a eliminar: ", "ID inválido. Ingrese un número entero positivo.")
        niveles = [n for n in niveles if n.id != int(id)]

        # Convertir los objetos Nivel de vuelta a diccionarios para guardarlos en el JSON
        data = [nivel.__dict__ for nivel in niveles]
        self.json_file.save(data)
        print("Nivel educativo eliminado exitosamente.")
        time.sleep(2)

    def consult(self):
        """Muestra la lista de niveles educativos o busca uno específico."""
        borrarPantalla()
        gotoxy(0, 2)

        data = self.json_file.read()
        niveles = [Nivel(n['id'], n['nivel']) for n in data]

        if not niveles:
            print("No hay niveles educativos registrados.")
            return

        while True:
            print("\n--- Consultar Niveles Educativos ---")
            print("1. Listar todos los niveles educativos")
            print("2. Buscar nivel educativo por ID")
            print("3. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                for nivel in niveles:
                    print(f"ID: {nivel.id}, Nombre: {nivel.nivel}, Estado: {'Activo' if nivel.active else 'Inactivo'}")
            elif opcion == '2':
                id = self.valida.solo_numeros("Ingrese el ID del nivel educativo a buscar: ", "ID inválido. Ingrese un número entero positivo.")
                nivel = next((n for n in niveles if n.id == int(id)), None)
                if nivel:
                    print(f"ID: {nivel.id}, Nombre: {nivel.nivel}, Estado: {'Activo' if nivel.active else 'Inactivo'}")
                else:
                    print("Nivel educativo no encontrado.")
            elif opcion == '3':
                break
            else:
                print("Opción inválida. Intente de nuevo.")