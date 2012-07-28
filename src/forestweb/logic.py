#-*- coding: utf-8 -*-
#import util
import model
import dbaccess

def analizar_madera(madera):
    """ 
    Analiza la compatibilidad una  madera. 
    Determinando todos los usos compatibles 
    """ 
    print madera.nombre
    usos_analisis = []
    usos_compatibles = []
    for uso in dbaccess.buscar_usos():
        analisis = [] # para cada uso
        uso_analisis = {} # tiene dos partes
        presentacion = {}
        # se retornarán solo las propiedades que constan en el 'uso'
        #for k in uso.propiedades.keys():...
        for pbd in dbaccess.buscar_propiedades():
            k = pbd.get('id_propiedad') 
            # propiedad no existe en 'uso' o en 'madera'
            if not uso.propiedades.get(k) or not madera.propiedades.get(k):
                #c = model.Compatibilidad(k,None,None)
                c = model.Compatibilidad(k,True,False)
            elif not uso.propiedades[k].min and madera.propiedades[k] <= uso.propiedades[k].max:
                c = model.Compatibilidad(k,True,pbd.get('obligatoria',''))
            elif not uso.propiedades[k].max and madera.propiedades[k] >= uso.propiedades[k].min:
                c = model.Compatibilidad(k,True,pbd.get('obligatoria',''))
            elif uso.propiedades[k].min <= madera.propiedades[k] <= uso.propiedades[k].max:
                c = model.Compatibilidad(k,True,pbd.get('obligatoria',''))
            else:
                c = model.Compatibilidad(k,False,pbd.get('obligatoria',''))
            analisis.append(c)
        #se puede colocar todo el objeto uso....
        uso_analisis['nombre_uso'] = uso.nombre
        uso_analisis['analisis'] = analisis
        usos_analisis.append(uso_analisis)
        # por necesidad de presentacion del nombre del uso
        presentacion = procesar_presentacion(analisis)
        presentacion['nombre_uso'] = uso.nombre
        print uso.nombre, presentacion
        incompatibles = incompatibilidades(analisis)
        #if len(uso.propiedades) > 0 and len(incompatibles) == 0:
        if len(incompatibles) == 0:
            usos_compatibles.append(uso)
            print incompatibles,'Es COMPATIBLE :)'
        else:
            print incompatibles,'Es INCOMPATIBLE :('
    return ( usos_compatibles, usos_analisis )

def procesar_presentacion(analisis):
    pres = {}
    for c in analisis:
        value = 'C' if c.compatible else 'I'
        if c.obligatoria:
            value = '[%s]'%value
        pres [c.propiedad] = value
    return pres

def incompatibilidades(analisis):
    incompatibilidades = []
    for c in analisis:
        # Si es obligatoria y la propiedad de la madera es incompatible
        if c.obligatoria and not c.compatible:
            incompatibilidades.append(c)
    return incompatibilidades

def analizar_uso(uso):
    """ 
    Determina todas las maderas que son compatibles con un uso dado
    """ 
    maderas_analisis = []
    maderas_compatibles = []
    for madera in dbaccess.buscar_maderas():
        madera_analisis = {}
        analisis = []
        for pbd in dbaccess.buscar_propiedades():
            k = pbd.get('id_propiedad')
            if not madera.propiedades.get(k) or not uso.propiedades.get(k): 
                c = model.Compatibilidad(k,None,None)
            elif not uso.propiedades[k].min and madera.propiedades[k] <= uso.propiedades[k].max:
                c = model.Compatibilidad(k,True,pbd.get('obligatoria',''))
            elif not uso.propiedades[k].max and madera.propiedades[k] >= uso.propiedades[k].min:
                c = model.Compatibilidad(k,True,pbd.get('obligatoria',''))
            elif uso.propiedades[k].min <= madera.propiedades[k] <= uso.propiedades[k].max:
                c = model.Compatibilidad(k,True,pbd['obligatoria'])
            else:
                c = model.Compatibilidad(k,False,pbd['obligatoria'])
            analisis.append(c)
        madera_analisis['nombre_madera'] = madera.nombre
        madera_analisis['analisis'] = analisis
        maderas_analisis.append(madera_analisis)
        print uso.nombre,'=>',madera.nombre
        print procesar_presentacion(analisis)
        incompatibles = incompatibilidades(analisis)
        print incompatibles
        if len(madera.propiedades) > 0 and len(incompatibles) == 0:
            maderas_compatibles.append(madera)
            print 'Es COMPATIBLE :)'
        else:
            print 'Es INCOMPATIBLE :('
    return ( maderas_compatibles, maderas_analisis )


if __name__ == '__main__':
    pass
