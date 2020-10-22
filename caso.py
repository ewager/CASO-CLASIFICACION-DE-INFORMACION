#!/usr/bin/python

'''
Caso - JSON y CSV en Base de Datos 
'''

###########################################
# Autor
###########################################
__author__ = 'Ewald Hollstein <ewager@gmail.com>'                                                                                            
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
from pymongo import MongoClient # modulo para trabajar con bd
#verificamos  que exista una instancia de mongodb activa
try:
    conn = MongoClient()
except:
    print("[ERROR] El script necesita MongoDB")

###########################################
# Cargamos archivo de configuracion
###########################################
configParser = ConfigParser.RawConfigParser() #cargamos metodo
configFilePath = './config.cfg' #cargamos archivo de  configuracion
configParser.read(configFilePath)

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
    # Abrimos conexion a BD
    ###########################################
    db = conn.database
    collection = db.caso

    ###########################################
    # Abrimos archivo
    ###########################################
    with open(file_csv, 'r') as f:
        data = f.readlines()

	write_log("INFO: Procesando Archivo: %s" % file_csv)

    	for line in data:
            # parsing de archivo csv
       	    index = line.split(';')

            #creamos array con datos normalizados para insertar
            data = {
                    "row_id":index[0],
                    "user_id":index[1],
                    "user_state":index[2],
                    "user_manager":index[3],
                    "email_owner":index[4],
                    "email_manager":index[5],
                    "bd":index[6]
                    }

            # Insertamos  datos
            collection.insert_one(data)
            write_log("[OK]: Datos Insertados CSV2MongoDB: %s " % data)

###########################################
# Funcion para leer archivo json
###########################################
def read_json(file_json):

    ###########################################
    # Abrimos conexion a BD
    ###########################################
    db = conn.database
    collection = db.caso

    ###########################################
    # Abrimos archivo
    ###########################################
    with open(file_json, 'r') as f:
        data_json = json.load(f)
        for line in data_json['bd']:

            #creamos array con datos normalizados para insertar
            data = {
                    "nombre_BD":line['nombre_BD'],
                    "Clasificacion":line['Clasificacion']
                    }

            # Insertamos  datos
            collection.insert_one(data)
            write_log("[OK]: Datos Insertados JSON2MongoDB: %s " % data)

###########################################
# Funcion para leer documentos insertados mongodb 
###########################################
def query_mongo():

    ###########################################
    # Abrimos conexion a BD
    ###########################################
    db = conn.database
    collection = db.caso

    # Query
    check = db.list_collection_names()
    if "caso" in check:
        cursor = collection.find()
        for record in cursor:
            write_log("Registro Encontrado: %s" % record)
    else:
        write_log("[Error] MongoDB")


###########################################
# Main
###########################################
if __name__ == "__main__":                                                                                                     
	###########################################
	# Argumentos
	###########################################
        parser = argparse.ArgumentParser(description='Ingresa archivo CSV, JSON.')
        parser.add_argument('-j','--json', help='JSON File',required=False)
        parser.add_argument('-c','--csv',help='CSV File', required=False)
        parser.add_argument('-s','--show',help='Show Collections Documents', required=False)
        args = parser.parse_args()

        if args.csv and path.exists(args.csv): #verificamos que se encuentre el argumento y que el archivo exista
                write_log("Archivo CSV %s existe para ser procesado." % args.csv)
                read_csv(args.csv)

        if args.json and path.exists(args.json): #verificamos que se encuentre el argumento y que el archivo exista
                write_log("Archivo JSON %s existe para ser procesado." % args.json)
                read_json(args.json)

        if args.show:
                write_log("Listando Documentos Insertados...")
                query_mongo()
