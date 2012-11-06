#-*- coding: utf-8 -*-

"""
Scripts para administrar la base de datos mongodb como
un servidor de archivos desde python.
"""
import os
import platform

""" Parametros del servidor """
DIRECTORIO = os.path.abspath(os.path.dirname(__file__))
MONGODIR=os.path.abspath('{0}/../../mongodb'.format(DIRECTORIO))
HOST='127.0.0.1'
PORT=27019

""" Obtención de la architectura correcta """
sistema = platform.system().lower()
arquitectura = platform.architecture()[0]
if 'linux' in sistema and '64' in arquitectura:
    SERVERDIR = "{0}/linux64".format(MONGODIR)
elif 'linux' in sistema and '32' in arquitectura:
    SERVERDIR = "{0}/linux32".format(MONGODIR)
elif 'windows' in sistema and '64' in arquitectura:
    SERVERDIR = "{0}/win64".format(MONGODIR)
elif 'windows' in sistema and '32' in arquitectura:
    SERVERDIR = "{0}/win32".format(MONGODIR)
    
def start():
    try:
    ###lock = '{0}/data/mongod.lock'.format(SERVERDIR)
    ###if os.path.isfile(lock):
    ###    os.remove(lock)
        os.system("{0}/mongod --auth --dbpath={1}/data  --logpath={2}/log/mongod.log --bind_ip={3} --port={4} --logappend &".format(SERVERDIR, SERVERDIR, SERVERDIR, HOST, PORT))
        print u'Servidor de Base de Datos iniciado satisfactoriamente !!!'
    except Exception, ex:
        print "Error al iniciar servidor mongodb: ", ex

def stop():
    try:
        command = 'db.shutdownServer()'
        # Unicamente se puede apagar el servidor desde la base de datos 'admin'.
        os.system('{0}/mongo {1}:{2}/admin --quiet -u mongoadmin -p humongous --eval "{3}"'.format(
                SERVERDIR, '127.0.0.1', PORT, command))
        print u'Servidor de Base de Datos apagado correctamente !!!'
    except: 
        print 'Error al apagar servidor mongodb.'

def winservice():
    """ Instalar MongoDB como un servicio windows"""
    os.system("{0}/mongod --install --auth --dbpath={1}/data  --logpath={2}/log/mongod.log --bind_ip=127.0.0.1 --port={4} ".format(SERVERDIR, SERVERDIR, SERVERDIR, HOST, PORT))
    os.system("net start MongoDB")
    print "Instalado el Servicio MongoDB satisfactoriamente"

def setup():
    try:
        # Instala la base de datos
        os.system("{0}/mongorestore --dbpath {1}/data {2}/../install/data/mongobackup".format(
                SERVERDIR, SERVERDIR, MONGODIR
                ))
        # Eliminar posibles problemas de bloqueo
        lock = '{0}/data/mongod.lock'.format(SERVERDIR)
        if os.path.isfile(lock):
            os.remove(lock)
        # Arranca el servidor de BD
        start() 
        # Extraño: si el codigo de add_admin se coloca aquí el cliente produce un error
        addadmin()
        print u"Instalación de la Base de Datos satisfactoria !!!"
    except Exception, ex:
        print "Errores al instalar la Base de Datos forestweb: ", ex

def add_admin():
    """ Agregar el usuario administrador del servidor MongoDB """
    os.system('{0}/mongo {1}:{2}/admin --eval "db.addUser(\'mongoadmin\',\'humongous\')" --quiet'.format(SERVERDIR, '127.0.0.1', PORT))
