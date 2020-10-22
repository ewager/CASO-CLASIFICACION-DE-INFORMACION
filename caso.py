#!/usr/bin/python

'''
Caso - JSON y CSV en Base de Datos 
'''

###########################################
# Instalar  librerias requeridas
# pip install $nombre_de_modulo
###########################################
# librerias
###########################################
import re #regular expresions
import argparse #argumentos 
import datetime #log file
import ConfigParser # archivo  de config
import os # verificacion de archivos
import os.path # verificacion de archivos
from os import path
import json #modulo para procesar json

###########################################
# Autor
###########################################
__author__ = 'Ewald Hollstein <ewager@gmail.com>'                                                                                            

###########################################
configParser = ConfigParser.RawConfigParser() #cargamos metodo
configFilePath = './config.cfg' #cargamos archivo de  configuracion
configParser.read(configFilePath)
###########################################

###########################################
# Variables
###########################################
debug = configParser.get('variables globales', 'debug')
logging = configParser.get('variables globales', 'log')

###########################################
# SET PATH de ejecucion
###########################################
home = os.getcwd() # obtenemos path actual de ejecucion
os.chdir(home) # nos cambiamos  al path

###########################################
# Funcion para verificar archivos
###########################################
if not path.exists(configFilePath):
    print "ERROR, archivo " + configFilePath + " no existe"
elif not path.exists(logging):
    print "ERROR, archivo " + logging + " no existe"

###########################################
# Funcion para escribir log
###########################################
def write_log(data):
    
	format = "%a %b %d %H:%M:%S %Y"
	get_date = datetime.datetime.today()
	date = get_date.strftime(format)

	if debug == '0':
		with open(logging, "a") as log:
			log.write(date + " " + data + "\n")
	else:
		print date + " " + data

###########################################
# Funcion para leer archivo csv
###########################################
def read_csv(file_csv):

    ###########################################
    # Abrimos archivo
    ###########################################
    with open(file_csv, 'r') as f:
        data = f.readlines()

    	for line in data:
	    if line.startswith("#"):
		continue

	    write_log("INFO: Procesando Registro: %s" % line)
       	    index = line.split(';')

	    ###########################################
	    # Parseamos el archivo
	    ###########################################
	    row_id= index[0]
	    user_id= index[1]
	    user_manager= index[2]
	    email_owner = index[3]
	    email_manager = index[5]

            write_log("ROW_ID: %s USER_ID: %s USER_MANAGER: %s EMAIL_OWNER: %s EMAIL_MANAGER: %s" % (row_id,user_id,user_manager,email_owner,email_manager))

###########################################
# Funcion para leer archivo json
###########################################
def read_json(file_json):

    ###########################################
    # Abrimos archivo
    ###########################################
    with open(file_json, 'r') as f:
        data = json.load(f)
        for p in data['bd']:
            print ('nombre_BD: ' + p['nombre_BD'] + ' ' + 'Clasificacion: ' +  p['Clasificacion'])


###########################################
# Funcion para insertar data
###########################################

###########################################
# Funcion para enviar correo
###########################################

###########################################
# Main
###########################################
if __name__ == "__main__":                                                                                                     
	###########################################
	# Argumentos
	###########################################
        parser = argparse.ArgumentParser(description='Ingresa archivo CSV, JSON.')
        parser.add_argument('-j','--json', help='JSON File',required=True)
        parser.add_argument('-c','--csv',help='CSV File', required=True)
        args = parser.parse_args()

        if args.csv and path.exists(args.csv): #verificamos que se encuentre el argumento y que el archivo exista
                write_log("Archivo CSV %s existe para ser procesado." % args.csv)
                read_csv(args.csv)

        else:
                write_log("Archivo CSV %s no existe." % args.csv)

        if args.json and path.exists(args.json): #verificamos que se encuentre el argumento y que el archivo exista
                write_log("Archivo JSON %s existe para ser procesado." % args.json)
                read_json(args.json)

        else:
                write_log("Archivo JSON %s no existe." % args.json)

