#-*- coding: utf-8 -*-
import collections
import dbaccess

#codificaciones = {'muy_bajo':1,'bajo':2,'medio':3,'alto':4,'muy_alto':5,'excelente':1,'bueno':2,'regular':3,'pobre':4}

Rango = collections.namedtuple('Rango', 'min max')
Compatibilidad = collections.namedtuple('Compatibilidad','propiedad compatible obligatoria')

'''
class Propiedad:
    """ Propiedad Fisica, Mecanica o Anatomica de la Madera """
    def __init__(self,nombre='',clase='',obligatoria=False,unidad='',diccionario=None, categoria=None):
        if diccionario:
            self.__dict__ = diccionario
        else:
            self.id_propiedad = '0'
            self.nombre = nombre
            self.clase = clase
            self.obligatoria = obligatoria
            self.categoria = categoria
            self.unidad = unidad
            #self.codificaciones = {} ...

    def __str__(self):
        return '%s',self.nombre
'''

class Madera(object):
    
    def __init__(self,nombre=''):
        self.id_madera = '0'
        self.nombre = nombre
        self.especie = 'NN'
        # los valores de las propiedades de una madera son flotantes
        self.__valores = {}
        # las propiedades de la madera son enteros
        self.__propiedades = {}

    def actualizar_valores(self,valores):
        """ Agrega nuevas propiedades o cambia los valores de las ya existentes """ 
        self.__valores.update(valores)
        self.set_valores(self.__valores)

    def set_valores(self,valores):
        """ Al cambiar los valores de la madera se recodifican sus propiedades en base a esos valores """
        self.__valores = valores
        for (id_propiedad,valor) in valores.items():
            propiedad = dbaccess.buscar_propiedad(id_propiedad)
            nombre_codif = ''
            if propiedad.get('clase') == u'tecnológica':
                """ Recorremos las codificaciones que tiene la propiedad """
                for (codif,rango) in propiedad['codificaciones'].items():
                    if not rango.min and valor <= rango.max:
                        nombre_codif = codif
                        break
                    if not rango.max and valor >= rango.min: 
                        nombre_codif = codif
                        break
                    if rango.min <= valor <= rango.max:
                        nombre_codif = codif
                        break
            elif propiedad.get('clase') == u'anatómica':
                # valor 'str', es el nombre ya codificado que viene del <select> html
                # valor es ya el nombre codificado desde la vista
                nombre_codif = valor
            # se supone que se encuentra una sola codificacion
            consulta = dbaccess.codificaciones(nombre=nombre_codif)
            if consulta: 
                codificacion = consulta[0]
                self.__propiedades[id_propiedad] = codificacion.get('valor')

    def get_valores(self):
        return self.__valores

    def get_propiedades(self):
        return self.__propiedades

    valores = property(get_valores,set_valores)
    #propiedades es de solo lectura, no puede cambiar ???
    #No se deben cambiar directamente las propiedades sino a través de los valores ???"""
    propiedades = property(get_propiedades)

    def __str__(self):
        return '%s: %s' % (self.nombre.encode('utf-8'), self.propiedades)

    def __repr__(self):
        return '%s'%self.nombre.encode('utf-8')


class Uso(object):

    def __init__(self,nombre=''):
        self.id_uso = '0'
        self.nombre = nombre
        # las propiedades de los usos son rangos de enteros
        self.propiedades = {}

    def __str__(self):
        return '%s'%self.nombre.encode('utf-8')

    def __repr__(self):
        return '%s'%self.nombre.encode('utf-8')

if __name__ == '__main__':
    print 'Only testing...'
    print Madera()
    r = Rango(3,4)
    print r
    print r.min
    print r.max
