"""
Scripts para administrar la base de datos mongodb como
un servidor de archivos desde python.
"""

import os

""" Parametros del servidor """
DIRECTORIO = os.path.abspath(os.path.dirname(__file__))
SERVERDIR=os.path.abspath('{0}/../../mongodb'.format(DIRECTORIO))
HOST='localhost'
PORT=27019

def start():
    lock = '{0}/data/mongod.lock'.format(SERVERDIR)
    #if os.path.isfile(lock):
    #    os.remove(lock)
    os.system("{0}/mongod --dbpath={1}/data  --logpath={2}/log/mongod.log --bind_ip={3} --port={4} --logappend &".format(
        SERVERDIR, SERVERDIR, SERVERDIR, HOST, PORT))
    
def shutdown():
    # mongod --shutdown --dbpath=...
    os.system("{0}/mongod --shutdown --dbpath={1}/data ".format(
        SERVERDIR, SERVERDIR))

# Verificacion Inicial
start()
