from utilities import green_color, blue_color, purple_color, reset_color, red_color, borrarPantalla, linea, gotoxy, cyan_color
from Icrud import Icrud
from crudStudents import CrudStudents
from crudTeacher import CrudTeacher
from crudCourses import CrudCourses
from crudGrades import CrudGrades 
from clsJson import JsonFile
from datetime import date
from components import Valida, Menu
import datetime
import os
import time
import platform

opc = ''
while opc != '6':
    borrarPantalla()
    menu_main = Menu(f"{purple_color}Menu Sistema Académico", [f"{cyan_color}1) Estudiantes", "2) Profesores", "3) Cursos", "4) Notas", "5) Salir"]) 
    opc = menu_main.menu()

    if opc == '1':
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            menu_students = Menu(f"{purple_color}Menu Estudiantes {reset_color}", [f"{cyan_color}1) Crear", "2) Actualizar", "3) Eliminar", "4) Consultar", "5) Salir"])
            opc1 = menu_students.menu()
            crud = CrudStudents()
            if opc1 == '1':
                crud.create()
            elif opc1 == '2':
                crud.update()
            elif opc1 == '3':
                crud.delete()
            elif opc1 == '4':
                crud.consult()
            print("Regresando al menu principal")

    elif opc == '2':
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            menu_teachers = Menu("Menu Profesores", [f"{cyan_color}1) Crear", "2) Actualizar", "3) Eliminar", "4) Consultar", "5) Salir"])
            opc2 = menu_teachers.menu()
            crud = CrudTeacher()
            if opc2 == '1':
                crud.create()
            elif opc2 == '2':
                crud.update()
            elif opc2 == '3':
                crud.delete()
            elif opc2 == '4':
                crud.consult()
            print("Regresando al menu principal")

    elif opc == '3':
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            menu_courses = Menu("Menu Cursos", [f"{cyan_color}1) Crear", "2) Actualizar", "3) Eliminar", "4) Consultar", "5) Salir"])
            opc3 = menu_courses.menu() 
            crud = CrudCourses()
            if opc3 == '1':
                crud.create()
            elif opc3 == '2':
                crud.update()
            elif opc3 == '3':
                crud.delete()
            elif opc3 == '4':
                crud.consult()
            print("Regresando al menu principal")

    elif opc == '4': # Notas
        opc4 = ''
        while opc4 != '5':
            borrarPantalla()
            menu_grades = Menu("Menu Calificaciones", ["1) Crear", "2) Actualizar", "3) Eliminar", "4) Consultar", "5) Salir"])
            opc4 = menu_grades.menu() 
            crud = CrudGrades() 
            if opc4 == '1':
                crud.create()
            elif opc4 == '2':
                crud.update()
            elif opc4 == '3':
                crud.delete()
            elif opc4 == '4':
                crud.consult()
            print("Regresando al menu principal")

    elif opc == '5':  # Opción para salir
        break

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()