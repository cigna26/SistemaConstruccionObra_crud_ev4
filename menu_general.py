from os import system
from data_base_MD5 import DatabaseMD5

db = DatabaseMD5()

while True:
    elige = input('\n Elije una opcion: \n\
        \t Ingresar sesion(i)\n\
        \t Crear usuario(c)\n\
        \t Fin(f)\n\
        \t ==> \n ').lower()
    if elige == 'i':
        db.ingresar()
    elif elige == 'c':
        db.crearUsuario()

    elif elige == 'f':
        print('Fin. Saliendo del programa..,')
        break
    else:
        print('Error de opción')
        input('Pulse Enter para continuar...')
        system('cls')        
