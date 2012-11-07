#-*- coding: utf-8 -*-

import web
import mongodb
# Iniciamos el Sevidor de Base de Datos
# TODO: Se podria crear como un servicio del sistema 
mongodb.start()

import logic
import model
# Conexión implicita a la BD luego de iniciar servidor
import dbaccess

urls = ('/','portada',
        '/login','login',
        '/index','index',
        '/cambiarclave','cambiarclave',
        '/propiedades','propiedades',
        '/usos','usos',
        '/maderas','maderas',
        '/editptecnologica','editptecnologica',
        '/editpanatomica','editpanatomica',
        '/edituso','edituso',
        '/editmadera','editmadera',
        '/codificar','codificar',
        '/analizar_madera','analizar_madera',
        '/analizar_uso','analizar_uso',
        '/seleccionar_uso','seleccionar_uso',
        '/seleccionar_madera','seleccionar_madera',
        )

aplicacion = web.application(urls,globals())
renderizador = web.template.render('templates',globals={'dbcodif':dbaccess.codificaciones})
if web.config.get('_session') is None:
    session = web.session.Session(aplicacion, web.session.DiskStore('sessions'),
                                  initializer={'lang':'es_ES'})
    web.config._session = session
else:
    session = web.config._session

session.login = 0 

def logeado():
    if session and 'login' in session and session.login == 1 :
        return True
    else:
        return False

class portada:
    def GET(self):
        if 'salir' in web.input():
            # cerrar session
            session.login = 0
            session._save()
            session.kill()
            # Detener el servidor de BD
            mongodb.stop()
        return renderizador.portada()


class login:
    def GET(self):
        return renderizador.login()

    # autenticación
    def POST(self):
        import hashlib
        form = web.input()
        # para implementaciones futuras
        # pwdhash = hashlib.md5(form.password).hexdigest() 
        pwd = form.password
        check = dbaccess.buscar_usuario(form.username, pwd)
        if check:
            session.loggedin = True
            session.username = form.username
            session.password = pwd
            session.login = 1
            web.seeother('/index')
        else: 
            return "<h2> Nombre de usuario o contraseña incorrectos <br/>" +"<a href='/login'> Regresar </a> </h2>"


class index:
    def GET(self):
        if logeado():
            return renderizador.index()
        else:
            return "<h3> Necesita Autenticarse </h3>"

class cambiarclave:
    def GET(self):
        return renderizador.cambiarclave(session)

    def POST(self):
        form = web.input()
        if form.password == session.password:
            if form.newpassword1  == form.newpassword2:
                if dbaccess.cambiar_clave(session.username,form.newpassword2):
                    print "<h3> Clave cambiada con éxito </h3>"
                else:
                    print "Error al cambiar la clave"
        
class propiedades:
    def GET(self):
        propiedades = dbaccess.buscar_propiedades()
        # TODO: check why not work
        # return renderizador.propiedades(propiedades)
        return renderizador.propiedades(dbaccess.bd.propiedades.find())


class editptecnologica:
    def GET(self):
        propiedad = None
        if 'id_propiedad' in web.input():
            id_propiedad = web.input().id_propiedad
            propiedad = dbaccess.buscar_propiedad(id_propiedad)
        if not propiedad:
            propiedad = dict()
            propiedad['id_propiedad'] = dbaccess.contar_propiedades() + 1
        cods = dbaccess.codificaciones(clase='tecnológica')
        return renderizador.editptecnologica(propiedad,cods)

    # grabar propiedad tecnológica
    def POST(self):
        form = web.input()        
        propiedad = dict()
        propiedad['id_propiedad'] = form.id_propiedad
        propiedad['nombre'] = form.nombre
        propiedad['abreviatura'] = form.abreviatura
        propiedad['categoria'] = form.categoria
        # obligatorio
        propiedad['clase'] = 'tecnológica'
        if form.get('obligatoria',''):
            propiedad['obligatoria'] = True
        else:
            propiedad['obligatoria'] = False
        codificaciones = dict()
        for c in dbaccess.codificaciones(clase='tecnológica'):
            # valores para cada codificacion
            val_min = form.get(str(c['valor']) + '-min','')
            val_max = form.get(str(c['valor']) + '-max','')
            if val_min or val_max:
                if val_min and val_max:
                    val_min = float(val_min)
                    val_max = float(val_max)
                    # asegurando efectivamente el orden de los valores
                    a,b = val_min, val_max
                    val_min, val_max = min(a,b), max(a,b)
                elif val_min and (not val_max or val_max == ''): 
                    val_max = None
                    val_min = float(val_min)                    
                elif (not val_min or val_min == '') and val_max:
                    val_min = None
                    val_max = float(val_max)
                codificaciones[c['nombre']] = model.Rango(val_min,val_max)
            propiedad['codificaciones'] = codificaciones
        print propiedad
        dbaccess.grabar_propiedad(propiedad) 


class editpanatomica:
    def GET(self):
        propiedad = None
        if 'id_propiedad' in web.input():
            id_propiedad = web.input().id_propiedad
            propiedad = dbaccess.buscar_propiedad(id_propiedad)
        if not propiedad:
            propiedad = dict()
            propiedad['id_propiedad'] = dbaccess.contar_propiedades() + 1
        cods = dbaccess.codificaciones(clase='anatómica')
        return renderizador.editpanatomica(propiedad,cods)

    # grabar propiedad anatómica
    def POST(self):
        form = web.input()        
        propiedad = dict()
        propiedad['id_propiedad'] = form.id_propiedad
        propiedad['nombre'] = form.nombre
        propiedad['abreviatura'] = form.abreviatura
        # de cajón
        propiedad['clase'] = 'anatómica'
        if form.get('obligatoria',''):
            propiedad['obligatoria'] = True
        else:
            propiedad['obligatoria'] = False
        codificaciones = dict()
        for c in dbaccess.codificaciones(clase='anatómica'):
            # valores para cada codificacion
            if form[c['nombre']]:
                codificaciones[c['nombre']] = form[c['nombre']]
        propiedad['codificaciones'] = codificaciones
        dbaccess.grabar_propiedad(propiedad) 

class maderas:
    def GET(self):
        maderas = dbaccess.buscar_maderas()
        propiedades = dbaccess.buscar_propiedades() 
        return renderizador.maderas(propiedades,maderas)
        ### return renderizador.maderas(propiedades, dbaccess.bd.maderas.find())

class editmadera:
    def GET(self):
        """ Lectura de una madera """
        ### propiedades = dbaccess.buscar_propiedades()
        # TODO: Custiones de acceso a la BD
        propiedades = dbaccess.bd.propiedades.find()
        madera = None
        if 'id_madera' in web.input():
            id_madera = web.input().id_madera
            madera = dbaccess.buscar_madera(id_madera)
        if not madera:
            madera = model.Madera()
            madera.id_madera = dbaccess.contar_maderas() + 1
        return renderizador.editmadera(madera,propiedades)

    def POST(self):
        """ Graba una madera """
        m = model.Madera()
        data = web.input()
        m.id_madera = data.id_madera
        m.nombre = data.nombre
        # Se debe recorrer todas las propiedades existentes
        for p in dbaccess.buscar_propiedades():
            id_p = p.get('id_propiedad')
            valor =  data['prop-'+id_p]
            if valor: 
                m.propiedades[id_p] = int(data['prop-'+id_p])
        dbaccess.grabar_madera(m)


class edituso:
    def GET(self):
        # TODO: Cuestiones de acceso a BD
        ### propiedades = dbaccess.buscar_propiedades()
        propiedades = dbaccess.bd.propiedades.find()
        uso = None
        if 'id_uso' in web.input():
            id_uso = web.input().id_uso
            uso = dbaccess.buscar_uso(id_uso)
        if not uso:
            uso = model.Uso()
            uso.id_uso = dbaccess.contar_usos()  + 1
        return renderizador.edituso(uso,propiedades)
    
    def POST(self):
        """ Graba un objeto Uso con el respectivo mapeo """
        u = model.Uso()
        data = web.input()
        u.id_uso = data.id_uso
        u.nombre = data.nombre
        # se debe recorrer todas las propiedades existentes
        for p in dbaccess.buscar_propiedades():
            id_p = p.get('id_propiedad')
            val_min = data['%s-min' % id_p]
            val_max = data['%s-max' % id_p]
            if val_min or val_max:
                if val_min and val_max:
                    val_min = int(val_min)
                    val_max = int(val_max)
                    # asegurando efectivamente el orden de los valores
                    a,b = val_min, val_max
                    val_min, val_max = min(a,b), max(a,b)
                elif not val_max: 
                    #val_max = None ...
                    val_min = int(val_min)                    
                elif not val_min:
                    #val_min = None ...
                    val_max = int(val_max)
                u.propiedades[id_p] = model.Rango(val_min,val_max)
        dbaccess.grabar_uso(u) 

class usos:
    def GET(self):
        usos = dbaccess.buscar_usos()
        propiedades = dbaccess.buscar_propiedades()
        return renderizador.usos(propiedades,usos)
        ### return renderizador.usos(propiedades, dbaccess.bd.usos.find())

class codificar:
    """ Codifica los valores de las propiedades de una madera """
    def GET(self):
        madera = model.Madera()
        madera.nombre = web.input().nombre
        data = web.input()
        valores = {}
        """ 'v' es cada 'valor' de la propiedad que viene de la vista """
        for (k,v) in data.items():
            if k.startswith('valor') and v:
                # si se trata de una propiedad tencnológica
                if v.replace('.','').isdigit():
                    valores[k.split('-')[1]] = float(v)
                # si se trata de una propiedad anatómica
                else:
                    valores[k.split('-')[1]] = v
        # En este momento se codifican las propiedades
        print valores
        madera.set_valores(valores)
        web.header('Content-type','application/json')
        print madera.propiedades
        import json
        return json.dumps(madera.propiedades)

class analizar_madera:
    def GET(self):
        propiedades = dbaccess.buscar_propiedades()
        #madera = model.Madera()
        madera = None
        if 'id_madera' in web.input():
            id_madera = web.input().id_madera
            madera = dbaccess.buscar_madera(id_madera)
        if madera:
            if len(madera.propiedades) > 0:
                usos_compatibles, usos_analisis = logic.analizar_madera(madera)
                return renderizador.analizar_madera(propiedades,madera,usos_compatibles,usos_analisis)
            else:
                return "La madera << %s >> no tiene propiedades que analizar" % madera.nombre
        

class analizar_uso:
    def GET(self):
        propiedades = dbaccess.buscar_propiedades()
        uso = None
        if 'id_uso' in web.input():
            id_uso = web.input().id_uso
            uso = dbaccess.buscar_uso(id_uso)
        if uso:
            if len(uso.propiedades) > 0:
                maderas_compatibles, maderas_analisis = logic.analizar_uso(uso)
                return renderizador.analizar_uso(propiedades,uso,maderas_compatibles,maderas_analisis)
            else:
                return "El uso << %s >> no tiene propiedades que analizar" % uso.nombre

class seleccionar_uso:
    def GET(self):
        return renderizador.seleccionar_uso(dbaccess.buscar_usos())

class seleccionar_madera:
    def GET(self):
        return renderizador.seleccionar_madera(dbaccess.buscar_maderas())

if __name__ == '__main__':
    aplicacion.run()
