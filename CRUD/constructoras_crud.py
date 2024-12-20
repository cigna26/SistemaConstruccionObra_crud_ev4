import mysql.connector
from os import system

import time

class Constructoras(): 
    def __init__(self):  
        self.conexion = mysql.connector.connect( 
            host = 'localhost',
            user = 'root',
            password = 'carlos123',
            database = 'unidad'
        )
        self.cursor = self.conexion.cursor()    
    
    
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()
        
    #Lista
    def list_constructoras(self): 
        sql = 'select * from constructoras'
        try:
            self.cursor.execute(sql)
            repu = self.cursor.fetchall()
            print((
            f"{'ID Constructora':10}"
            f"{'Fono ':20}"
            f"{'Email ':12}"
            ))
            for rep in repu:
                print(f"{rep[0]:10}{rep[1]:20}{rep[2]:12}")
        except Exception as err:
            print(err)
            
    #CREATE
    def create_constructora(self):
        id_constructora = input('Ingrese ID de la constructora= \n')
        
        #if not id_constructora.isalnum() or len(id_constructora) != 10:
        #    raise ValueError("El código debe ser un valor alfanumérico de exactamente 10 caracteres.")
        
        sql1 = 'select idConstructora from constructoras where idConstructora ='+repr(id_constructora)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone() == None:
                fono = input('Fono = \n') 
                email = input('Email \n')
                sql2 = "insert into constructoras values("+repr(id_constructora)+","+repr(fono)+","+repr(email)+")"
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()  
                    print("Constructora creada exitosamente") 
                except Exception as err:
                    self.conexion.rollback()
                    print("Error al crear la constructora:", err)
            else:
                print("Ya existe una constructora con este ID. No se puede crear la constructora.")
        except Exception as err:
            print("Error al verificar el ID de la constructora:", err)  
            
    #READ
    def read_constructora(self):    
        id_buscar = input('Ingrese ID de constructora a buscar = \n')
    
        sql = 'select * from constructoras where idconstructora = '+repr(id_buscar) 
        #repr agrega cremillas al cod
        try:
            self.cursor.execute(sql)
            rep = self.cursor.fetchone()
            if rep is not None:
                print((
                f"{'ID Constructora':10}"
                f"{'Fono ':20}"
                f"{'Email ':12}"
                ))
                
                print(f"{rep[0]:10}{rep[1]:20}{rep[2]:12}")
            else:
                print('Id no existe en la base de datos')
        except Exception as err:
            print("Error al realizar la consulta", err) 
            
    #UPDATE
    def update_constructoras(self):
        #Llamar una funcion dentro de otra
        self.list_constructoras()
        
        id_buscar = input('Ingrese ID de constructora que desea actualizar = \n')
        sql1 = 'select * from constructoras where idconstructora='+repr(id_buscar)
        try:
            self.cursor.execute(sql1)
            rep=self.cursor.fetchone()
            if rep!= None:
                print("Información actual de la constructora:")
                print("---------------------------------------------------------")
                print((
                    f"{'ID Constructora':20}"
                    f"{'Fono ':20}"
                    f"{'Email ':12}"
                    ))
                print(f"{rep[0]:20}{rep[1]:20}{rep[2]:12}")
                print("---------------------------------------------------------")
                ##Da la opcion de elegir que desea modificar
                elige=input('\n Que desea modificar?\n fono(f)\n email(e)\n').lower()
                if elige=='f':
                    campo='fono'
                    nuevo=input('Ingrese nuevo fono = ')
                    print("Fono actualizado exitosamente.")
                if elige=='e':
                    campo='email'
                    nuevo=input('Ingrese nuevo email = ')
                    print("Email actualizado exitosamente.")

                sql2 = 'update constructoras set '+campo+'='+repr(nuevo)+' where idconstructora='+repr(id_buscar)
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print("Actualización realizada con éxito.")
                except Exception as err:
                    self.conexion.rollback()
                    print("No existe una constructora con ese ID. Intente con otro ID")
            else:
                print('No existe ese código')
        except Exception as err: 
            print("Error al buscar la constructora:", err)
            
    #DELETE        
    def delete_constructora(self):
        #Llamar una funcion dentro de otra
        self.list_constructoras()
        
        id_buscar = input('Ingrese ID de constructora que desea eliminar = \n')
        sql1 = 'select * from constructoras where idconstructora='+repr(id_buscar)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone() != None:
                print("------------------------------------------------")
                print("La constructora con ID", id_buscar, "existe. Verificando si está asociada con alguna obra...")
                print("------------------------------------------------")
                sql2 = 'select * from obras where idConstructora ='+repr(id_buscar)
                try:
                    self.cursor.execute(sql2)
                    if self.cursor.fetchone()!= None:
                        time.sleep(1)
                        print('No se puede eliminar, porque esta asociada con Obras')
                    else:
                        sql3 = 'delete from constructoras where idconstructora='+repr(id_buscar)
                        try:
                            self.cursor.execute(sql3)
                            self.conexion.commit()
                            time.sleep(1)
                            print("Constructora eliminada exitosamente.")
                        except Exception as err:
                            self.conexion.rollback()
                            time.sleep(1)
                            print("Error al eliminar la constructora:", err)
                except Exception as err:
                    time.sleep(1)
                    print("Error al verificar las obras asociadas:", err)
            else:
                print("No existe una constructora con este ID. Intente con otro ID")
        except Exception as err:
            print("Error al buscar la constructora:", err)
            
    #Menu para ser llamado en DataBaseMD5 
    def menu_constructoras(self):
        while True:
            elige = input('\n Elije una opcion: \n\
                        \t Listar Constructoras(l)\n\
                        \t Buscar una Constructora(b)\n\
                        \t Crear una Constructora(c)\n\
                        \t Actualizar una Constructora(a)\n\
                        \t Eliminar una Constructora(e)\n\
                        \t Fin(f)\n\
                        \t ==> \n ').lower()
            #Si elige una opcion de CRUD
            if elige == 'l':
                self.list_constructoras()
            elif elige == 'c':
                self.create_constructora()
            elif elige == 'b':
                self.read_constructora()  
            elif elige == 'a':
                self.update_constructoras()
            elif elige == 'e':
                self.delete_constructora()
            elif elige == 'f':
                print('Fin')
                self.cerrarBD()
                break
            else:
                print('Error de opción')
            input('Pulse Enter para continuar...')
            system('cls')