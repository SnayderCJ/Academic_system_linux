from utilities import green_color, blue_color, purple_color, reset_color,red_color, borrarPantalla,linea, gotoxy
from Icrud import Icrud
from crudStudents import CrudStudents
from crudTeacher import CrudTeacher
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
    menu_main = Menu("Menu Sistema Académico", ["Estudiantes", "Profesores", "Cursos", "Matrículas", "Calificaciones", "Salir"])
    opc = menu_main.menu()
    
    if opc == '1':
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            menu_clients = Menu("Menu Estudiantes", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
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
            menu_teachers = Menu("Menu Profesores", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
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
            menu_sales = Menu("Menu ventas", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
            opc3 = menu_sales.menu()
            crud = CrudSales()
            if opc3 == '1':
                crud.create()
            elif opc3 == '2':
                crud.update()
            elif opc3 == '3':
                crud.delete()
            elif opc3 == '4':
                crud.consult()
    
    elif opc == '4':
        opc4 = ''
        while opc4 != '5':
            borrarPantalla()
            menu_company = Menu("Menu compañía", ["Crear", "Actualizar", "Eliminar", "Consultar", "Salir"])
            opc4 = menu_company.menu()
            crud = CrudCompany()
            if opc4 == '1':
                crud.create()
            elif opc4 == '2':
                crud.update()
            elif opc4 == '3':
                crud.delete()
            elif opc4 == '4':
                crud.consult()
                print("Regresando al menu principal")

    print("Regresando al menu principal")

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()