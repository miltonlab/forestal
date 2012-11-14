#-*- coding: utf-8 -*-

import time
import re
from pymongo.connection import Connection
from pymongo.son_manipulator import SONManipulator
from pymongo.errors import AutoReconnect

conexion = None
bd = None
try:
    conexion = Connection('localhost:27019')
    bd = conexion.bosqueseco
    # TODO: Cambiar configuracion a través de archivos
    bd.authenticate('forestweb','forestweb')
    print "Conexión satisfactoria a la BD"
except AutoReconnect as ex:
    print u"Error de conexión a la BD: {0}".format(str(ex))
    # Intento de reconexion después de 1 segundo
    time.sleep(1)
    conexion = Connection('localhost:27019')
    bd = conexion.bosqueseco
    # TODO: Cambiar configuracion a través de archivos
    bd.authenticate('forestweb','forestweb')
    print "Conexión satisfactoria a la BD"

import model

#testing ...
def reconectar():
    conexion = Connection('localhost')
    #BD = conexion.forestal
    bd = conexion.bosqueseco
    bd.authenticate('forestweb','forestweb')
    
def cambiar_clave(usuario,clave_nueva):
    try:
        bd.usuarios.update({'username':usuario},
                           {'username':usuario,'password':clave_nueva})
        return True
    except Exception as e: 
        print "Error al cambiar clave: %s" % str(e)
        return False


def buscar_usuario(username,password):
    return bd.usuarios.find_one({'username':username,'password':password})


def buscar_propiedad(id_propiedad=None,codigo=None):
    """ Devuelve una sola propiedad de la base de datos """
    if id_propiedad:
        return  bd.propiedades.find_one({'id_propiedad':id_propiedad})
    elif codigo:
        return  bd.propiedades.find_one({'codigo':codigo})

def contar_propiedades():
    return bd.propiedades.count()

def contar_maderas():
    return bd.maderas.count()

def contar_usos():
    return bd.usos.count()

def buscar_propiedades(nombre='.*',codigo='.*'):
    if nombre=='.*': nombre = re.compile(nombre)
    if codigo=='.*': codigo = re.compile(codigo)
    if nombre == '.*' and codigo == '.*':
        cursor = bd.propiedades.find()
    else:
        cursor = bd.propiedades.find( {'nombre':nombre,'codigo':codigo} ).sort('nombre',1)
    ###
    return [p for p in cursor]

def buscar_usos(nombre='.*'):
    """ Debe retornar una lista de objetos model.Uso """
    nombre = re.compile(nombre)
    usos = []
    ### for u in bd.usos.find({'nombre':nombre}).sort('nombre',1):
    for u in bd.usos.find().sort('nombre',1):
        uso = model.Uso()
        uso.__dict__ = u
        usos.append(uso)
    usos.sort(lambda u1,u2: cmp(u1.nombre, u2.nombre))
    return usos

def buscar_uso(id_uso):
    """ Devuelve un solo uso de la base de datos """
    u_props = bd.usos.find_one({'id_uso':id_uso})
    u = None
    if u_props: 
        u = model.Uso()
        u.__dict__ = u_props
    return u

def buscar_maderas(nombre='.*'):
    """ Debe retornar una lista de objetos model.Madera """
    nombre = re.compile(nombre)
    maderas = []
    ### for m in bd.maderas.find({'nombre':nombre}).sort('nombre',1):
    for m in bd.maderas.find().sort('nombre',1):
        madera = model.Madera()
        madera.__dict__ = m
        maderas.append(madera)
    return maderas

def buscar_madera(id_madera):
    """ Devuelve una sola madera de la base de datos """
    m = None
    m_props = bd.maderas.find_one({'id_madera':id_madera})
    if m_props: 
        m = model.Madera()
        m.__dict__ = m_props
    return m

def grabar_propiedad(propiedad):
    """ Se debe tener en cuenta la estructura del diccionario propiedad """
    p_bd = bd.propiedades.find_one({'id_propiedad':propiedad['id_propiedad']})
    if p_bd:
        p_bd.update(propiedad)
        bd.propiedades.save(p_bd)
    else:
        # siguiente 'id'
        id_propiedad = str(bd.propiedades.count() + 1)
        propiedad['id_propiedad'] = id_propiedad
        bd.propiedades.save(propiedad)

def grabar_madera(madera):
    """ Se debe tener en cuenta la estructura del diccionario de madera """
    m_bd = bd.maderas.find_one({'id_madera':madera.id_madera})
    if m_bd:
        m_bd.update(madera.__dict__)
        bd.maderas.save(m_bd)
    else:
        # siguiente 'id'
        id_madera = str(bd.maderas.count() + 1)
        madera.id_madera = id_madera
        bd.maderas.save(madera.__dict__)

def grabar_uso(uso):
    """ Se debe tener en cuenta la estructura del diccionario de uso """
    u_bd = bd.usos.find_one({'id_uso':uso.id_uso})
    if u_bd:
        u_bd.update(uso.__dict__)
        bd.usos.save(u_bd)
    else:
        # siguiente 'id'
        id_uso = str(bd.usos.count() + 1)
        uso.id_uso = id_uso
        bd.usos.save(uso.__dict__)

def codificaciones(clase='.*',nombre='.*'):
    """ 
    Obtiene las codificaciones de las propiedades por clase y/o nombre
    Se devuelve el resultado en una lista común para aislar esta capa.
    """
    lista = list()
    if clase == '.*': clase = re.compile(clase)
    if  nombre == '.*': nombre = re.compile(nombre)
    codsbd = bd.codificaciones.find( {'clase':clase,'nombre':nombre} )
    for c in codsbd:
        lista.append(dict(c))
    return lista

class TransformerRango(SONManipulator):
    def transform_incoming(self,son,collection):
        for (key,value) in son.items():
            if isinstance(value,model.Rango):
                # un objeto model.Rango se mapea hacia un diccionario 
                son[key] = value._asdict()
            elif isinstance(value,dict):
                son[key] = self.transform_incoming(value,collection)
        return son

    def transform_outgoing(self,son,collection):
        for (key,value) in son.items():
            if isinstance(value,dict):
                # se trata de un model.Rango
                if value.keys() == ['max','min']:
                    son[key] = model.Rango(value['min'],value['max'])
                else:
                    son[key] = self.transform_outgoing(value,collection)
        return son

# mapeador entre objetos model.Rango y diccionarios
if bd is not None:
    bd.add_son_manipulator(TransformerRango())    



