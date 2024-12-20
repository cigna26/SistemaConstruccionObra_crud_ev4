from datetime import datetime
import mysql.connector 
from os import system
import time
from fpdf import FPDF


class Obras(): 
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
        
    def generar_pdf(self, registros):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Título
            pdf.cell(200, 10, txt="Listado de Obras", ln=True, align="C")

            # Encabezados
            encabezados = ["ID", "Nombre", "Constructora", "Estado", "Fecha inicio"]
            for encabezado in encabezados:
                pdf.cell(40, 10, txt=encabezado, border=1)
            pdf.ln()

            # Contenido
            for registro in registros:
                for campo in registro:
                    pdf.cell(40, 10, txt=str(campo), border=1)
                pdf.ln()

            # Guardar el archivo
            pdf.output("listado_obras.pdf")
            print("PDF generado: listado_obras.pdf")
        
    def list_obras(self): 
        sql = 'select * from obras'
        try:
            self.cursor.execute(sql)
            repu = self.cursor.fetchall()

            # Encabezados en consola
            print((
                f"{'Cod. Obra ':10}"
                f"{'Id Construct. ':20}"
                f"{'Descrip. Obra ':20}"
                f"{'Costo Obra ':12}"
                f"{'Fecha Inicio ':12}"
            ))

            # Imprimir registros en consola
            for rep in repu:
                print(f"{rep[0]:12}{rep[1]:20}{rep[2]:20}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")

            # Preguntar si se desea generar el PDF
            opcion = input("Desea generar un PDF con este listado? (s/n): ").lower()
            if opcion == 's':
                self.generar_pdf(repu)

        except Exception as err:
            print("Error al listar obras:", err)
            
        # sql = 'select * from obras'
        # try:
        #     self.cursor.execute(sql)
        #     repu = self.cursor.fetchall()
        #     print((
        #     f"{'Cod. Obra ':10}"
        #     f"{'Id Construct. ':20}"
        #     f"{'Descrip. Obra ':20}"
        #     f"{'Costo Obra ':12}"
        #     f"{'Fecha Inicio ':12}"
        #     ))
        #     for rep in repu:
        #         print(f"{rep[0]:12}{rep[1]:20}{rep[2]:20}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")
        # except Exception as err:
        #     print(err)
            
    #CREATE
    def create_obras(self):
        codigo_obra = input('Ingrese ID de la Obra = \n')
        sql1 = 'select codigoObra from obras where codigoObra =' + repr(codigo_obra)

        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone() is None:
                # Pedir el ID de la Constructora
                id_constructora = input('Ingrese ID de la Constructora = \n')
                sql2 = 'select idConstructora from constructoras where idConstructora =' + repr(id_constructora)
                
                
                try:
                    self.cursor.execute(sql2)
                    if self.cursor.fetchone() is not None:  # Si el id_constructora existe
                        print("---------------------------------------------")
                        print("Validación de ID de la constructora correcta.")
                        print("---------------------------------------------")

                        descripcionObra = input('Descripcion de la obra = \n')
                        costo = int(input('Costo de la Obra = \n'))
                        fechaInicio = input('Fecha de inicio Obra (aaaa-mm-dd) = \n')

                        # Validar y formatear la fecha
                        try:
                            fecha_inicio = datetime.strptime(fechaInicio, '%Y-%m-%d')
                            fecha_inicio_sql = fecha_inicio.strftime('%Y-%m-%d')
                        except ValueError:
                            print("Formato de fecha incorrecto. Debe ser aaaa-mm-dd.")
                            return
                        
                        print("---------------------------------------------")
                        print("Preparando para insertar en la base de datos...")
                        # Insertar en la base de datos
                        sql3 = "insert into obras (codigoObra, idConstructora, descripcionobra, costo, fechainicio) VALUES (" \
                            + repr(codigo_obra) + ", " + repr(id_constructora) + ", " + repr(descripcionObra) + ", " + repr(costo) + ", " + repr(fecha_inicio_sql) + ")"

                        try:
                            self.cursor.execute(sql3)
                            self.conexion.commit()
                            time.sleep(1) 
                            print("Obra agregada exitosamente...")
                            print("---------------------------------------------")

                        except Exception as err:
                            self.conexion.rollback()
                            print("Error al insertar la obra:", err)
                    else:
                        print("---------------------------------------------")
                        print("El ID de la Constructora no existe. Por favor, verifique y vuelva a intentarlo.")
                        print("---------------------------------------------")

                except Exception as err:
                    print("Error al verificar el ID de la Constructora:", err)
            else:
                print('Ya existe una obra con este ID.')
        except Exception as err:
            print("Error al verificar el código de la obra:", err)

            
            
    #READ
    def read_obras(self):    
        codigo_obra = input('Ingrese codigo a buscar = \n')
    
        sql = 'select * from obras where codigoobra = '+repr(codigo_obra) 
        #repr agrega cremillas al cod
        try:
            self.cursor.execute(sql)
            rep = self.cursor.fetchone()
            if rep is not None:
                print((
                f"{'Codigo Obra':10}"
                f"{'Ide Constructora ':20}"
                f"{'Descripcion ':12}"
                f"{'Costo ':12}"
                f"{'Fecha Inicio':12}"
                ))
                
                print(f"{rep[0]:10}{rep[1]:20}{rep[2]:20}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")
            else:
                print('Codigo no existe en la base de datos')
        except Exception as err:
            print("Error al realizar la consulta", err)
            
            
    #UPDATE
    def update_obras(self):
        
        #Llamar una funcion dentro de otra
        self.list_obras()
        
        codigo_obra = input('Ingrese codigo a buscar = \n')
        sql1 = 'select * from obras where codigoobra ='+repr(codigo_obra)
        try:
            self.cursor.execute(sql1)
            rep=self.cursor.fetchone()
            if rep!= None:
                print((
                f"{'Codigo Obra':13}"
                f"{'Id Constructora ':20}"
                f"{'Descripcion':15}"
                f"{'Costo ':12}"
                f"{'Fecha Inicio':12}"
                ))
                
                print(f"{rep[0]:13}{rep[1]:20}{rep[2]:15}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")
                elige=input('\n Que desea modificar?\n Descripcion(d)\n Costo(c)\n').lower()
                if elige=='d':
                    campo='descripcionObra'
                    nuevo=input('Ingrese nueva Descripcion=')
                if elige=='c':
                    campo='costo'
                    nuevo=input('Ingrese nuevo costo=')
                

                sql2 = 'update obras set '+campo+'='+repr(nuevo)+' where codigoobra='+repr(codigo_obra)
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print("---------------------------------------------")
                    print("Actualizando la base de datos con modificaciones...")
                    time.sleep(1)
                    print("La obra fue actualizada con éxito.")
                    print("---------------------------------------------")

                except Exception as err:
                    self.conexion.rollback()
                    print("Error al actualizar la obra:", err)
            else:
                print('No existe ese código')
        except Exception as err: 
            print("Error al buscar la obra:", err)
            
    #Menu para ser llamado en DataBaseMD5 
    def menu_obras(self):
        while True:
            elige = input('\n Elije una opcion: \n\
                \t Listar Obras(l)\n\
                \t Buscar una Obra(b)\n\
                \t Crear una Obra(c)\n\
                \t Actualizar una Obra(a)\n\
                \t Fin(f)\n\
                \t ==> \n ').lower()
            #Si elige una opcion de CRUD
            if elige == 'l':
                self.list_obras()
            elif elige == 'c':
                self.create_obras()
            elif elige == 'b':
                self.read_obras()
            elif elige == 'a':
                self.update_obras()
                        
            elif elige == 'f':
                print('Fin')
                self.cerrarBD()
                break
            else:
                print('Error de opción')
            input('Pulse Enter para continuar...')
            system('cls')
    