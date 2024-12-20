import pymysql
from tabulate import tabulate
from pwinput import pwinput
from hashlib import md5
import time

from os import system

class DatabaseMD5():
    def __init__(self):
        self.conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='carlos123',
            database='unidad'
        )
        self.cursor = self.conexion.cursor()

    def cerrarDB(self):
        self.cursor.close()
        self.conexion.close()

    def login(self):
        nombre = input('Ingrese nombre del usuario = ')
        password = pwinput('Ingrese password = ')
        passwordEnc = md5(password.encode('utf-8')).hexdigest()
        return nombre, passwordEnc
    
    def crearUsuario(self):
        nom,passw = self.login()
        sql1='select * from usuarios where nombre='+repr(nom)
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result==None:
                sql2='insert into usuarios values('+repr(nom)+','+repr(passw)+')'
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print('Usuario creado exitosamente')
                except Exception as err:
                    self.conexion.rollback()
                    print("Error al intentar crear el usuario:", err)
            else:
                print('Ya existe ese nombre de usuario')
        except Exception as err:
            print("Error al verificar si el usuario ya existe:", err)

    def ingresar(self):
        nom,passw = self.login()
        sql1='select * from usuarios where nombre='+repr(nom)+' and password = '+repr(passw)
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result is not None:
                
                print("Ingreso exitoso, accediendo al menú general...")
                time.sleep(1) 
                #Se traen las clases 
                #Para llamado a los menus
                from CRUD.constructoras_crud import Constructoras
                from CRUD.obras_crud import Obras
                
                #Se renombra las clases
                cs = Constructoras()
                ob = Obras()
                
                #Bucle menu
                while True:
                    elige = input('\n Elije una opcion: \n\
                        \t Menu Constructoras(c)\n\
                        \t Menu Obras(o)\n\
                        \t Fin(f)\n\
                        \t ==> \n ').lower()
                    #Si elige la opcion de menu constructoras
                    if elige == 'c':
                        cs.menu_constructoras()
                    #Si elige la opcion de menu obras
                    elif elige == 'o':
                        ob.menu_obras()
                        
                    elif elige == 'f':
                        print('Fin. Saliendo al Login de usuario')
                        time.sleep(1)
                        break
                    else:
                        print('Error de opción, elija una opcion valida')    
                    input('Pulse Enter para continuar...')
                    system('cls')

            else:
                print('Usuario o contraseña incorrectos. Intente nuevamente.')
        except Exception as err:
            print("Error al verificar usuario:", err)
            self.menu_principal()
