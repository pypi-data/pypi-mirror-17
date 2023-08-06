# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as et


def relationMembers(**kwargs):
    """
    Este metodo lee la definicion de los metodos de un
    lado de la relacion.

    Parametros:
        version: version de metodos por defecto, standard
        part: lado de la relacion (to o from)
        filter: dimodelionario de booleanos de selemodelion de version
        dictionary: dimodelionario de valores a utilizar en la evaluacion

    Retorna:

        None en caso de error
        Array de definicion de metodos.
    """
    doc = '{0}Members.xml'.format(kwargs['part'])
    path = os.path.join(os.getcwd(), 'plugin', 'models', 'relation',
        kwargs.get('version', 'standard'), doc)
    key = kwargs.get('filter', None)
    if not os.path.isfile(path):
        print('{0} is missing'.format(path))
        return None
    try:
        tree = et.parse(path)  # retorna et.ElementTree
        root = tree.getroot()  # retorna et.Element
        dictionary = kwargs.get('dictionary', {})
        defs = root.find('definitions')
        if defs is not None:
            for d in defs:
                text = d.findtext('.')
                for x, y in [text.split('=')]:
                    v = y.format(**dictionary)
                    if v in ['True', 'False']:
                        v = eval(v)
                    dictionary[x] = v
        members = root.find('members')
        if members is None:
            print('missing members')
            return None
        result = []
        for member in members:
            keys = {}
            for x in member.keys():
                keys[x] = member.get(x).format(**dictionary)
                if x == 'type':
                    keys[x] = eval(keys[x], dictionary)
            result.append(keys)
        return result
    except Exception, e:
        print('Exception {msg} failed reading {p}'.format(
            msg=e.message, p=path))
        return None


def relationMethods(**kwargs):
    """
    Este metodo lee la definicion de los metodos de un
    lado de la relacion y los crea.

    Parametros:
        version: version de metodos por defecto, standard
        part: lado de la relacion (to o from)
        filter: dimodelionario de booleanos de selemodelion de version
        dictionary: dimodelionario de valores a utilizar en la evaluacion

    Retorna:

        None en caso de error
        Array de definicion de metodos.

    Comentarios:

        Los parametros de filtro permiten seleccionar entre
        diferentes versiones por ejemplo, de compatibilidad C++
        o niveles de seguridad (criticos), implementacion estatica
        presencia de metodos de busqueda, etc. Se selemodeliona
        el mejor matching y se excluyen aquellos metodos que
        no tengan ninguna version compatible con los filtros.

        Respecto de los simbolos utilizados en las declaraciones,
        esto es un aspecto pendiente de normalizar y documentar,
        ya que por ahora algunos de ellos dependen de la implementacion
        de los valores miembro.


    """
    import model
    doc = '{0}Methods.xml'.format(kwargs['part'])
    path = os.path.join(os.getcwd(), 'plugin', 'models', 'relation',
        kwargs.get('version', 'standard'), doc)
    key = kwargs.get('filter', None)
    if not os.path.isfile(path):
        print('{0} is missing'.format(path))
        return
    try:
        tree = et.parse(path)
        root = tree.getroot()
        dictionary = kwargs.get('dictionary', {})
        parent = dictionary.get('parent', None)
        if not parent:
            print('parent is missing')
            return        
        # read definitions and add it to dict
        defs = root.find('definitions')
        if defs is not None:
            for d in defs:
                text = d.findtext('.')
                for x, y in [text.split('=')]:
                    v = y.format(**dictionary)
                    if v in ['True', 'False']:
                        v = eval(v)
                    dictionary[x] = v

        methods = root.find('methods')
        if methods is None:
            print('missing methods')
            return
        #elements = methods.getchildren()
        #for method in elements:
        for method in methods:
            keys = {}
            for x in method.keys():
                v = method.get(x).format(**dictionary)
                if x == 'type' or v in {'True', 'False'}:
                    keys[x] = eval(v, dictionary)
                else:
                    keys[x] = v
            contents = method.findall('content')
            if contents is None:
                keys['content'] = ''
            else:
                best_match = -1
                best_content = None
                for content in contents:
                    #verificamos el filtro
                    f = content.get('filter', None)
                    ok = True
                    match = 0
                    if f is not None:
                        f = f.strip()[1:-1]  # quitamos los { y }
                        fk = dict([(x.strip(), (y.strip() == 'True'))
                            for x, y in [list(v.split(':')) for v in f.split(',')]])
                    # para pasar el filtro, deben coincidir los valores
                        for k in key:
                            if k in fk:
                                if key[k] != fk[k]:
                                    ok = False
                                    break
                                match += 1
                    if ok and match > best_match:
                        best_content = content
                        best_match = match
                if best_content is None:
                    keys['content'] = ''
                else:
                    keys['content'] = best_content.findtext('.').format(**dictionary)
            keys['type'] = model.cc.typeinst(**keys)
            keys.update({'parent': parent, 'readonly': True})
            m = model.cc.MemberMethod(**keys)
            # tomamos los argumentos
            args = method.find('args') or []
            for arg in args:
                akeys = {}
                for x in arg.keys():
                    v = arg.get(x).format(**dictionary)
                    if x == 'type' or v in ['True', 'False']:
                        akeys[x] = eval(v, dictionary)
                    else:
                        akeys[x] = v
                akeys['type'] = model.cc.typeinst(**akeys)
                akeys.update({'parent': m, 'readonly': True})
                model.cc.Argument(**akeys)
        return 
    except Exception, e:
        print('Exception {msg} failed reading {p}'.format(
            msg=e.message, p=path))
        return 


def relationClasses(**kwargs):
    """
    Realiza la construccion de las clases anidadas
    definidas por la relacion
    """
    import model
    doc = '{0}Classes.xml'.format(kwargs['part'])
    path = os.path.join(os.getcwd(), 'plugin', 'models', 'relation',
        kwargs.get('version', 'standard'), doc)
    key = kwargs.get('filter', None)
    if not os.path.isfile(path):
        print('{0} is missing'.format(path))
        return
    try:
        tree = et.parse(path)
        root = tree.getroot()
        dictionary = kwargs.get('dictionary', {})
        parent = dictionary.get('parent', None)
        if not parent:
            print('parent is missing')
            return
        # read definitions and add it to dict
        defs = root.find('definitions')
        if defs is not None:
            for d in defs:
                text = d.findtext('.')
                for x, y in [text.split('=')]:
                    v = y.format(**dictionary)
                    if v in ['True', 'False']:
                        v = eval(v)
                    dictionary[x] = v

        classes = root.find('classes')
        if classes is None:
            print('missing classes')
            return
        for _class in classes:
            keys = {}
            # leemos los atributos de la clase
            for x in _class.keys():
                keys[x] = _class.get(x).format(**dictionary)
            # ponemos atributos
            keys.update({'parent': parent, 'readonly': kwargs.get('readonly', True)})
            # creamos la clase
            cls = model.cc.Class(**keys)
            dictionary.update({cls.name: cls})
            # buscamos los tipos definidos en la clase
            types = _class.find('types')
            for type in types:
                keys = {}
                for x in type.keys():
                    keys[x] = type.get(x).format(**dictionary)
                keys.update({'parent': cls})
                t = model.cc.Type(**keys)
                dictionary.update({t.name: t})
            # buscamos los miembros
            members = _class.find("members")
            for member in members:
                keys = {}
                for x in member.keys():
                    keys[x] = member.get(x).format(**dictionary)
                    if x in ['type', 'static', 'const', 'volatile', 'virtual', 'ptr', 'ref', 'mutable']:
                        keys[x] = eval(keys[x], dictionary)
                keys['type'] = model.cc.typeinst(**keys)
                keys.update({'parent': cls})
                model.cc.MemberData(**keys)
            # constructores
            ctors = _class.find('ctors')
            for _ctor in ctors:
                keys = {'parent': cls, 'name': cls.name, 'autoargs': False}
                for x in _ctor.keys():
                    keys[x] = _ctor.get(x).format(**dictionary)
                    if x == 'inline':
                        keys[x] = eval(keys[x], dictionary)
                ctor = model.cc.Constructor(**keys)
                # argumentos
                args = _ctor.find('args')
                for arg in args:
                    keys = {'parent': ctor}
                    for x in arg.keys():
                        keys[x] = arg.get(x).format(**dictionary)
                        if x == 'type':
                            keys[x] = eval(keys[x], dictionary)
                    keys['type'] = model.cc.typeinst(**keys)
                    model.cc.Argument(**keys)

            # buscamos los metodos
            methods = _class.find('methods')
            for _method in methods:
                keys = {'parent': cls}
                for x in _method.keys():
                    k = keys[x] = _method.get(x).format(**dictionary)
                    if x == 'type':
                        if k:
                            keys[x] = eval(k, dictionary)
                        else:
                            keys[x] = dictionary[k]  # implicit type
                    elif k in ['True', 'False']:
                        keys[x] = eval(k, dictionary)

                contents = _method.findall('content')
                if contents is None:
                    keys['content'] = ''
                else:
                    best_match = -1
                    best_content = None
                    for content in contents:
                        #verificamos el filtro
                        f = content.get('filter', None)
                        ok = True
                        match = 0
                        if f is not None:
                            f = f.strip()[1:-1]  # quitamos los { y }
                            fk = dict([(x.strip(), (y.strip() == 'True'))
                                for x, y in [list(v.split(':')) for v in f.split(',')]])
                                # para pasar el filtro, deben coincidir los valores
                            for k in key:
                                if k in fk:
                                    if key[k] != fk[k]:
                                        ok = False
                                        break
                                    match += 1
                        if ok and match > best_match:
                            best_content = content
                            best_match = match
                    if best_content is None:
                        keys['content'] = ''
                    else:
                        keys['content'] = best_content.findtext('.').format(**dictionary)
                       
                keys['type'] = model.cc.typeinst(**keys)
                keys.update({'parent': cls})

                method = model.cc.MemberMethod(**keys)
                # argumentos
                args = _method.find('args')
                for arg in args:
                    keys = {}
                    for x in arg.keys():
                        keys[x] = arg.get(x).format(**dictionary)
                        if x in ['type', 'static', 'const', 'volatile', 'ptr', 'ref']:
                            keys[x] = eval(keys[x], dictionary)
                    keys['type'] = model.cc.typeinst(**keys)
                    keys.update({'parent': method})
                    model.cc.Argument(**keys)
            #destructor
            _dtor = _class.find('dtor')
            if _dtor:
                keys = {}
                for x in _dtor.keys():
                    keys[x] = _dtor.get(x).format(**dictionary)
                    if x in ['virtual', 'inline']:
                        keys[x] = eval(keys[x], dictionary)
                keys.update({'parent': cls, 'name': cls.name})
                model.cc.Destructor(**keys)

    except Exception, e:
        print('Exception {msg} failed reading {p}'.format(
            msg=e.message, p=path))
        return
