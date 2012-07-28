#-*- coding: utf-8 -*-
import xlrd
import model
import dbaccess

"""
Para cargar a la bd se debe llamar al metodo de grabación adecuado del módulo
'dbaccess' con cada uno de los objetos retornados por estos métodos.
"""

def load_tecnologicas_xls(file='archivos/PROPIEDADES.xls'):
    """ Carga propiedades físicas y mecánicas de la madera """
    propiedades = []
    campos = ['nombre','categoria','codigo','obligatoria','unidad','muy_bajo','bajo','medio','alto','muy_alto']
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_name('tecnologicas')
    for r in range(1,sheet.nrows):
        propiedad = {}
        id_propiedad = r if not dbaccess.buscar_propiedad(str(r)) else dbaccess.contar_propiedades() + len(propiedades) + 1
        # se agrega un id a la propiedad
        propiedad['id_propiedad'] = str(id_propiedad)
        propiedad['clase'] = 'tecnológica'
        propiedad['codificaciones'] = {}
        for c in range(sheet.ncols):
            cell = sheet.cell(r,c)
            if cell.value is not xlrd.empty_cell.value:
                if c < 5:
                    if sheet.cell(0,c).value == 'obligatoria':
                        propiedad['obligatoria'] = True if cell.value in ('Si','si','SI','sI') else False
                    else:
                        propiedad[sheet.cell(0,c).value.lower()] = cell.value
                # leemos las codificaciones
                else:
                    # espacios
                    cell.value = cell.value.replace(' ','')
                    # separador decimal
                    cell.value = cell.value.replace(',','.')
                    if '<' in cell.value:
                        maxval = float(cell.value.replace('<',''))
                        propiedad['codificaciones'][campos[c]] = model.Rango(None,maxval)
                    elif '>' in cell.value: 
                        minval = float(cell.value.replace('>',''))
                        propiedad['codificaciones'][campos[c]] = model.Rango(minval,None)
                    elif '-' in cell.value:
                        minval = float(cell.value.split('-')[0])
                        maxval = float(cell.value.split('-')[1])
                        propiedad['codificaciones'][campos[c]] = model.Rango(minval,maxval)
        propiedades.append(propiedad)
    return propiedades

def load_anatomicas_xls(file='archivos/PROPIEDADES.xls'):
    #""" Carga propiedades anatomicas de la madera """
    propiedades = []
    campos = ['nombre','obligatoria','codigo','excelente','bueno','regular','pobre']
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_name('anatomicas')
    for r in range(1,sheet.nrows):
        propiedad = {}
        propiedad['clase'] = 'anatómica'
        propiedad['codificaciones'] = {}
        id_propiedad = r if not dbaccess.buscar_propiedad(str(r)) else dbaccess.contar_propiedades() + len(propiedades) + 1
        propiedad['id_propiedad'] = str(id_propiedad)
        for c in range(0,sheet.ncols):
            value = sheet.cell(r,c).value
            if sheet.cell(0,c).value == 'nombre' or sheet.cell(0,c).value == u'codigo':
                propiedad[sheet.cell(0,c).value.lower()] = value
            elif sheet.cell(0,c).value == 'obligatoria':
                propiedad['obligatoria'] = True if value in ('Si','si','SI','sI') else False
            else:
                propiedad['codificaciones'][campos[c]] = value
        propiedades.append(propiedad)
    return propiedades

# Auxiliar, debe estar en el storage o BD
def buscar_propiedad(id_propiedad='0'):
    """ Devuelve una sola propiedad de la madera """
    l = [p for p in propiedades if p['id_propiedad'] == id_propiedad]
    return l[0] if l else None

def load_usos_xls_old(file='archivos/propiedades2.xls'):
    """ Carga los datos de los Rangos codificados de los usos """
    usos = []
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_name('usos')
    # usos
    for r in range(2,sheet.nrows,2):
        uso = model.Uso()
        for c in range(1,sheet.ncols):
            minval = sheet.cell(r,c).value
            maxval = sheet.cell(r+1,c).value
            #uso.propiedades[c] = {'min':minval ,'max':maxval}
            uso.propiedades[str(c)] = model.Rango(minval ,maxval)
        uso.nombre = sheet.cell(r,0).value
        usos.append(uso)
    return usos

def load_usos_xls(file='archivos/USOS.xls'):
    """ Carga los datos de los Rangos codificados de los usos """
    usos = []
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(0)
    # usos
    for r in range(3,sheet.nrows):
        if sheet.cell(r,0).value in ('','CODIGO','PRODUCTO A FABRICAR CON MADERA'): continue
        uso = model.Uso()
        uso.nombre = sheet.cell(r,0).value
        for c in range(1,sheet.ncols):
            if sheet.cell(r,c).value == '': continue
            value = sheet.cell(r,c).value
            minval = int(value.lower().split('a')[0])
            maxval = int(value.lower().split('a')[1])
            #uso.propiedades[c] = {'min':minval ,'max':maxval}
            #uso.propiedades[str(c)] = model.Rango(minval ,maxval)
            # usamos el encabezado para obtener el código de la propiedad
            cod = sheet.cell(2,c).value
            cod = cod.replace(' ','')
            rs = dbaccess.buscar_propiedades(codigo=cod)
            if rs[0]: 
                prop = rs[0]
                uso.propiedades[prop.get('id_propiedad')] = model.Rango(minval ,maxval)
            # otra alternativa
            #uso.propiedades[codigo] = model.Rango(minval ,maxval)
        usos.append(uso)
    return usos

def load_maderas_xls_old(file='archivos/propiedades2.xls'):
    """ Carga las propiedades codificadas ya establecidas de las maderas """
    maderas = []
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_name('maderas')
    for r in range(2,sheet.nrows):
        madera = model.Madera()
        for c in range(1,sheet.ncols):
            madera.propiedades[str(c)] = sheet.cell(r,c).value
        madera.nombre = sheet.cell(r,0).value
        maderas.append(madera)
    return maderas

def load_maderas_xls(file='archivos/MADERAS.xls'):
    """ Carga las propiedades codificadas ya establecidas de las maderas """
    maderas = []
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(0)
    for r in range(3,sheet.nrows):
        if sheet.cell(r,0).value in ('','CODIGO','PRODUCTO A FABRICAR CON MADERA'): continue
        madera = model.Madera()
        for c in range(1,sheet.ncols):
            if sheet.cell(r,c).value == '': continue
            val = int(sheet.cell(r,c).value)
            cod = sheet.cell(2,c).value.replace(' ','')
            rs = dbaccess.buscar_propiedades(codigo=cod)
            if rs[0]: 
                prop = rs[0]
                madera.propiedades[prop.get('id_propiedad')] = val
                madera.nombre = sheet.cell(r,0).value
        maderas.append(madera)
    return maderas

def sorted_keys(d,por_valor=False):
     """ Devuelve la lista de claves de un dict ornedada por clave o por valor """
     """ NOTA: En Python 3 no sería necesaria esta función """
     if por_valor:
         keys = sorted(d,key=lambda k: d[k])
     else:
         keys = sorted(d)
     return keys

def sorted_items(d,por_valor=False):
     """ Devuelve la lista de items de un dict ornedada por clave o por valor """
     """ NOTA: En Python 3 no sería necesaria esta función """
     if por_valor:
         items = sorted(d.items(),key=lambda item: item[1])
     else:
         items = sorted(d.items())
     return items

if __name__ == '__main__':
    pass
