import pandas as pd
import grafo as gf
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt


def angulo_calc(coord1, coord2, coord3):
    v1 = (coord2[0] - coord1[0], coord2[1] - coord1[1])
    v2 = (coord3[0] - coord2[0], coord3[1] - coord2[1])

    ang = (np.arccos(np.dot(v1, v2) /
           (np.linalg.norm(v1) * np.linalg.norm(v2)))) % 2*np.pi

    if ang < np.pi:
        return 'hacia la izquierda'
    elif ang > np.pi:
        return 'hacia la derecha'
    elif ang == np.pi:
        return 'recto'
    elif ang == 0:
        return 'recto'


def distancia_calc(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)/100


def tiempo_calc(coord1, coord2, tipo):
    dist = distancia_calc(coord1, coord2)  # Vamos a usar m/s -

    if tipo not in vias.keys():
        return dist / (50/3.6)
    else:
        return dist / (vias[tipo]/3.6)


def crear_grafos():

    global coordenadas, calles, codigos_calles, posiciones_mapa_dist, posiciones_mapa_tiempo, G_dist, G_tiempo

    for i in range(len(cruces.index)):
        fila = cruces.loc[i]

        coordenadas_cruce = (int(fila["Coordenada X (Guia Urbana) cm (cruce)"]),
                             int(fila["Coordenada Y (Guia Urbana) cm (cruce)"]))

        if coordenadas_cruce not in coordenadas:
            coordenadas[coordenadas_cruce] = set(
                [int(fila['Codigo de vía tratado']), int(fila['Codigo de via que cruza o enlaza'])])
            vertice = G_tiempo.agregar_vertice(coordenadas_cruce)
            vertice = G_dist.agregar_vertice(coordenadas_cruce)
            posiciones_mapa_dist[coordenadas_cruce] = coordenadas_cruce
            posiciones_mapa_tiempo[coordenadas_cruce] = coordenadas_cruce
        else:
            coordenadas[coordenadas_cruce].add(
                int(fila['Codigo de vía tratado']))
            coordenadas[coordenadas_cruce].add(
                int(fila['Codigo de via que cruza o enlaza']))

        if int(fila['Codigo de vía tratado']) not in calles:
            calles[int(fila['Codigo de vía tratado'])] = [
                [coordenadas_cruce], re.sub(" ", "", fila['Clase de la via tratado']), re.sub(r' +$', '', fila['Literal completo del vial tratado'])]

        else:
            if coordenadas_cruce not in calles[int(fila['Codigo de vía tratado'])][0]:
                calles[int(fila['Codigo de vía tratado'])
                       ][0].append(coordenadas_cruce)

            if calles[int(fila['Codigo de vía tratado'])][1] != re.sub(" ", "", fila['Clase de la via tratado']):
                print('ERROR')

        if int(fila['Codigo de via que cruza o enlaza']) not in calles:
            calles[int(fila['Codigo de via que cruza o enlaza'])] = [
                [coordenadas_cruce], re.sub(" ", "", fila['Clase de la via que cruza']), re.sub(r' +$', '', fila['Literal completo del vial que cruza'])]

        else:
            if coordenadas_cruce not in calles[int(fila['Codigo de via que cruza o enlaza'])][0]:
                calles[int(fila['Codigo de via que cruza o enlaza'])
                       ][0].append(coordenadas_cruce)

            if calles[int(fila['Codigo de via que cruza o enlaza'])][1] != re.sub(" ", "", fila['Clase de la via que cruza']) and int(fila['Codigo de via que cruza o enlaza']) != 176100:
                print('ERROR2')

        calle = re.sub(r' +$', '', fila['Literal completo del vial tratado'])
        calle2 = re.sub(
            r' +$', '', fila['Literal completo del vial que cruza'])

        if calle not in codigos_calles:
            codigos_calles[calle] = int(fila['Codigo de vía tratado'])
        else:
            if int(fila['Codigo de vía tratado']) == 906155:
                codigos_calles['CALLE DE LAFUENTE'] = int(
                    fila['Codigo de via que cruza o enlaza'])

            elif codigos_calles[calle] != int(fila['Codigo de vía tratado']):
                print('Hay un problema con la calle', calle)
                print('El código de la calle es', codigos_calles[calle], 'y el código de la fila es', int(
                    fila['Codigo de vía tratado']))

                break

        if calle2 not in codigos_calles:
            codigos_calles[calle2] = int(
                fila['Codigo de via que cruza o enlaza'])
        else:
            if int(fila['Codigo de via que cruza o enlaza']) == 906155:
                codigos_calles['CALLE DE LAFUENTE'] = int(
                    fila['Codigo de via que cruza o enlaza'])

            elif codigos_calles[calle2] != int(fila['Codigo de via que cruza o enlaza']):
                print('Hay un problema con la calle2', calle2)
                print('El código de la calle es', codigos_calles[calle2], 'y el código de la fila es', int(
                    fila['Codigo de via que cruza o enlaza']))

        # La CARRETERA / AUTOVIA de colmenar Viejo (176100) va cambiando de tipo de via cuando está en la columna de 'Codigo de via que cruza o enlaza'.
        # Cuando está en la columna de 'Codigo de vía tratado' es una carretera, así que se va a tomar ese tipo de vía.

        # Hay que quitarle los espacios a los tipos de via (hay problemas)

    # Ahora hay que crear las aristas entre los cruces

    # Dentro de cada calle, hay que buscar cuales están más cerca

    # Podemos sacar la distancia a todos los cruces de cada calle, y con eso sacamos los puntos mas lejanos entre si ( se da por hecho que son los más lejanos). Después desde uno de ellos sacamos las distancias y ordenamos uniendo vértices.
    # Vamos a hacer un diccionario de diccionarios para hallar las distanciass entre todos los cruces, de forma que sabemos todas. De ahí sacamos los pesos de cada arista.

    # A la hora de añadir a cada grafo una arista, el peso será diferente.

    for calle in calles.keys():
        if len(calles[calle][0]) == 2:
            G_dist.agregar_arista(calles[calle][0][0], calles[calle][0][1], {
                                  'id': calle, 'TIPO': calles[calle][1]}, distancia_calc(calles[calle][0][0], calles[calle][0][1]))
            G_tiempo.agregar_arista(calles[calle][0][0], calles[calle][0][1], {
                                    'id': calle, 'TIPO': calles[calle][1]}, tiempo_calc(calles[calle][0][0], calles[calle][0][1], calles[calle][1]))
        elif len(calles[calle][0]) == 1:
            pass
        else:
            # Vemos cuales son los puntos más lejanos entre si
            # Cogemos uno de ellos y sus peso al resto de vertices. Vamos añadiendo uno a uno en ese orden

            vertices_calle = calles[calle][0]

            distancias = {}  # Diccionario de diccionarios -> vertice: {vertice: distancia}
            # Nos guardamos la distancia máxima y el vértice
            dist_max = [0, None]

            tiempos = {}
            # Nos guardamos el tiempo máximo y el vértice
            tiempo_max = [0, None]

            for i in range(len(vertices_calle)):
                dist_act = {}
                tiempos_act = {}

                for j in range(len(vertices_calle)):

                    if i != j:

                        dist = distancia_calc(
                            vertices_calle[i], vertices_calle[j])
                        dist_act[vertices_calle[j]] = dist
                        if dist > dist_max[0]:
                            dist_max = [dist, vertices_calle[i]]

                        time = tiempo_calc(
                            vertices_calle[i], vertices_calle[j], calles[calle][1])
                        tiempos_act[vertices_calle[j]] = time
                        if time > tiempo_max[0]:
                            tiempo_max = [time, vertices_calle[i]]

                distancias[vertices_calle[i]] = dist_act
                tiempos[vertices_calle[i]] = tiempos_act

            # Ahora se sabe cual es el vértice más lejano, y se sabe la distancia a todos los demás vértices.
            # Seleccionamos nuestras distancias y tiempos

            distancia_max = distancias[dist_max[1]]
            tiempos_max = tiempos[tiempo_max[1]]

            # Hay que ordenar las distancias

            distancias_ordenadas = dict(
                sorted(distancia_max.items(), key=lambda x: x[1]))
            tiempos_ordenados = dict(
                sorted(tiempos_max.items(), key=lambda x: x[1]))

            vertices_ordenados_dist = list(distancias_ordenadas.keys())
            vertices_ordenados_tiempo = list(tiempos_ordenados.keys())

            # Ahora vamos a ir añadiendo los vértices al grafo seguidos

            for i in range(len(vertices_ordenados_dist)-1):
                G_dist.agregar_arista(vertices_ordenados_dist[i], vertices_ordenados_dist[i+1], {
                                      'id': calle, 'TIPO': calles[calle][1]}, distancias[vertices_ordenados_dist[i]][vertices_ordenados_dist[i+1]])
                G_tiempo.agregar_arista(vertices_ordenados_tiempo[i], vertices_ordenados_tiempo[i+1], {
                                        'id': calle, 'TIPO': calles[calle][1]}, tiempos[vertices_ordenados_tiempo[i]][vertices_ordenados_tiempo[i+1]])


def sacar_codigo_direccion(calle, numero):
    df = direcciones[direcciones['Codigo de via'] == calle]

    df2 = df[df['Literal de numeracion'] == numero]

    if len(df2) == 0:
        return None
    else:
        if len(df2) != 1:
            print('Hay más de un resultado')
            print(df2)
        else:
            return int(df2.loc[df2.index[0], 'Codigo de numero'])


def pedir_numero():
    error = True
    salir = False
    while error:
        try:
            tipo = (input('Tipo (NUM o KM): ')).upper()

            if tipo == '':
                return True, None

            elif tipo == 'NUM' or tipo == 'KM':
                numero = int(input('Número: '))
                if numero == '':
                    return True, None

                extra = (input('Extra ("-" si nada): ')).upper()

                if extra == '':
                    return True, None
                elif extra == '-':
                    extra = ''

                if tipo not in ['NUM', 'KM']:
                    print('Tipo no válido')
                    error = True
                else:
                    error = False
        except:
            print('Error en la entrada')
            error = True

    if tipo == 'NUM':
        string = 'NUM'
    else:
        string = 'KM.'

    if len(str(numero)) != 6:
        string += '0'*(6-len(str(numero))) + str(numero)
    else:
        string += str(numero)

    if extra != '':
        if tipo == 'KM':
            string += extra
        else:
            string += (' ' + extra)
    else:
        if tipo == 'NUM':
            string += '  '

    return salir, string


def sacar_vertice(codigo_direccion, tipo):
    df3 = direcciones[direcciones['Codigo de numero']
                      == codigo_direccion]
    direccion_info = df3.loc[df3.index[0]]
    calle = int(direccion_info['Codigo de via'])
    coord = (int(direccion_info['Coordenada X (Guia Urbana) cm']),
             int(direccion_info['Coordenada Y (Guia Urbana) cm']))

    if calle not in calles.keys():
        # Si la calle no está en nuestro dataset, se pide otra
        return [None, None, None, None]
    elif len(calles[calle][0]) == 1:
        # Si la calle solo tiene un vértice, se devuelve ese

        if tipo == 1:
            return [calles[calle][0][0], None, distancia_calc(calles[calle][0][0], coord), coord]
        else:
            return [calles[calle][0][0], None, tiempo_calc(calles[calle][0][0], coord, calles[calle][1]), coord]

    else:
        # Sacamos el vértice con menor distancia y vemos si hay arista hasta que se encuentre una

        vertices = calles[calle][0]

        # vamos a hacer un df

        if tipo == 1:
            distancias = {}
            distancias = {vertice: distancia_calc(
                vertice, coord) for vertice in vertices}

            # Ordenamos

            dist_ord = dict(sorted(distancias.items(),
                            key=lambda item: item[1]))

            # Ahora vamos comprobando si existe la arista

            vertices_ord = list(dist_ord.keys())

            existe = False

            for i in range(len(vertices_ord)):
                for j in range(i+1, len(vertices_ord)):
                    if vertices_ord[j] in G_dist.vertices[vertices_ord[i]].adyacencia:

                        existe = True

                        for arista in G_dist.aristas:
                            if arista.origen == vertices_ord[i] and arista.destino == vertices_ord[j]:
                                arista_dist = arista
                                break
                            else:
                                arista_dist = None
                        vertice = vertices_ord[i]
                        distancia = dist_ord[vertices_ord[i]]
                        break
                if existe:
                    break

            return [vertice, arista, distancia, coord]

        else:

            tiempos = {vertice: tiempo_calc(vertice, coord, calles[calle][1])
                       for vertice in vertices}

            # Ordenamos

            tiempos_ord = dict(
                sorted(tiempos.items(), key=lambda item: item[1]))

            # Ahora vamos comprobando si existe la arista

            vertices_ord_tiempo = list(tiempos_ord.keys())

            existe = False

            for i in range(len(vertices_ord_tiempo)):
                for j in range(i+1, len(vertices_ord_tiempo)):
                    if vertices_ord_tiempo[j] in G_tiempo.vertices[vertices_ord_tiempo[i]].adyacencia:

                        existe = True

                        for arista in G_tiempo.aristas:
                            if arista.origen == vertices_ord_tiempo[i] and arista.destino == vertices_ord_tiempo[j]:
                                arista_tiempo = arista
                                break
                            else:
                                arista_tiempo = None
                        vertice = vertices_ord_tiempo[i]
                        tiempo = tiempos_ord[vertices_ord_tiempo[i]]
                        break
                if existe:
                    break

            return [vertice, arista, tiempo, coord]


def menu():
    salir = False
    print('||||||| GPS |||||||\n')

    print('Siga las intrucciones para obtener una ruta.\nPara salir inserte en cualquier momento vacío\n')

    print('Elija tipo de busqueda: \n')
    print('    1. Por distancia')
    print('    2. Por tiempo')

    error = True
    while error:
        try:
            tipo = input('\nIngrese el numero del modo: ')

            if tipo == '':
                error = False
                return True, ''
            else:
                tipo = int(tipo)

            if tipo == 1 or tipo == 2:
                error = False

        except:
            print('No se ha introducido un numero valido')
            error = True

    print('\nAhora se va a seleccionar origen y destino. Por favor, introduzca el nombre completo, por ejemplo, "Calle de Sinesio Delgado"')

    if tipo == '':
        salir = True

    return salir, tipo
    pass


def origen_destino(tipo):
    salir = False
    error = True
    while error:
        try:
            calle_origen = (input('Introduce la calle de origen: ')).upper()

            if calle_origen == '':
                salir = True
                return salir, None, None

            codigo_calle_origen = codigos_calles[calle_origen]
            error = False

        except KeyError:
            print('No se ha encontrado la calle de origen')
            error = True

        if not error:

            error = True
            while error:
                salir, numero = pedir_numero()

                if salir:
                    return salir, None, None

                if numero not in direcciones[direcciones['Codigo de via'] == codigo_calle_origen]['Literal de numeracion'].values:
                    print('No se ha encontrado el número')
                    error = True
                else:
                    error = False
            codigo_origen = sacar_codigo_direccion(codigo_calle_origen, numero)
            data_origen = sacar_vertice(codigo_origen, tipo)
            if data_origen == [None]*4:
                print(
                    'Esta dirección de origen no está asociada a ninguna calle del dataset')
                error = True
            else:
                error = False

    error = True
    while error:
        try:
            calle_dest = (input('\nIntroduce la calle de destino: ')).upper()

            if calle_dest == '':
                salir = True
                return salir, None, None

            codigo_calle_dest = codigos_calles[calle_dest]
            error = False

        except:
            print('No se ha encontrado la calle de destino')
            error = True

        if not error:

            error = True
            while error:
                salir, numero = pedir_numero()

                if salir:
                    return salir, None, None

                if numero not in direcciones[direcciones['Codigo de via'] == codigo_calle_dest]['Literal de numeracion'].values:
                    print('No se ha encontrado el número')
                    error = True
                else:
                    error = False
            codigo_destino = sacar_codigo_direccion(codigo_calle_dest, numero)
            data_destino = sacar_vertice(codigo_destino, tipo)
            if data_destino == [None]*4:
                print(
                    'Esta dirección de destino no está asociada a ninguna calle del dataset')
                error = True
            else:
                error = False

    print('')
    return salir, data_origen, data_destino


def mostrar_camino(data_origen, data_destino, tipo):

    if tipo == 1:  # Con distancia
        tupla_camino = G_dist.camino_minimo_mejorado(
            data_origen[0], data_destino[0])

        camino_dist = tupla_camino[0]
        distancia_total = tupla_camino[1]

        if camino_dist == None:
            print('No hay camino entre estos dos puntos')
            return None
        else:
            print('\nEl camino más corto (distancia) es: ')
            if data_origen[1] == None:         # Se encuentra en un vértice
                string = ''
                cortes = ''
                for corte in coordenadas[data_origen[0]]:
                    cortes += calles[corte][2] + ', '
                string += f'\n1. Vamos al cruce de las calles {cortes} -> {round(data_origen[2],2)} metros'
                paso = 2
                distancia_seguida = 0
            else:  # Se encuentra en una arista
                string = ''
                calle_anterior = data_origen[1]
                distancia_seguida = data_origen[2]
                paso = 1

            i = 0

            while i <= len(camino_dist)-2:

                for aris in G_dist.aristas:
                    if aris.origen == camino_dist[i] and aris.destino == camino_dist[i+1]:
                        arista = aris

                # Es la primera, así que no tiene anterior -> entra solo si se encuentra en un vértice, ya que en el resto si tiene anterior
                if i == 0 and data_origen[1] == None:

                    distancia_seguida += arista.peso
                    calle_anterior = arista     # Se comprueba si el id coincide

                elif i == len(camino_dist)-2:  # Es la última, así que no tiene siguiente
                    if data_destino[1] == None:         # Se encuentra en un vértice
                        cortes = ''
                        for corte in coordenadas[data_destino[0]]:
                            cortes += calles[corte][2] + ', '
                        string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(distancia_seguida,2)} metros. Hasta llegar al cruce de {cortes}'
                        paso += 1
                        string += f'\n{paso}. Vamos desde donde estamos hasta nuestro destino -> {round(data_destino[2],2)} metros'
                    else:  # Se encuentra en una arista
                        if arista.data_arista['id'] == calle_anterior.data_arista['id']:
                            distancia_seguida += data_destino[2]
                            string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(distancia_seguida,2)} metros. Llegamos a nuestro destino'
                        else:

                            string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(distancia_seguida,2)} metros. Tomamos {angulo_calc(calle_anterior.origen, calle_anterior.destino, arista.destino)} {calles[arista.data_arista["id"]][2]}'
                            paso += 1
                            string += f'\n{paso}. Vamos por {calles[arista.data_arista["id"]][2]} -> {round(data_destino[2],2)} metros. Llegamos a nuestro destino'
                else:

                    if arista.data_arista['id'] == calle_anterior.data_arista["id"]:
                        distancia_seguida += arista.peso
                    else:
                        string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(distancia_seguida,2)} metros. Tomamos {angulo_calc(calle_anterior.origen, calle_anterior.destino, arista.destino)} {calles[arista.data_arista["id"]][2]}'
                        paso += 1
                        distancia_seguida = arista.peso
                        calle_anterior = arista

                i += 1
                # Lo primero sacamos los datos arista y comprobamos con la anterior si es la misma calle

    else:  # Con tiempo
        tupla_camino = G_tiempo.camino_minimo_mejorado(
            data_origen[0], data_destino[0])

        camino_tiempo = tupla_camino[0]
        tiempo_total = tupla_camino[1]

        if camino_tiempo == None:
            print('No hay camino entre estos dos puntos')
            return None
        else:
            print('\nEl camino más corto es: ')
            if data_origen[1] == None:         # Se encuentra en un vértice
                string = ''
                cortes = ''
                for corte in coordenadas[data_origen[0]]:
                    cortes += calles[corte][2] + ', '
                string += f'\n1. Vamos al cruce de las calles {cortes} -> {round(data_origen[2],2)} segundos'
                paso = 2
                tiempo_seguido = 0
            else:  # Se encuentra en una arista
                string = ''
                calle_anterior = data_origen[1]
                tiempo_seguido = data_origen[2]
                paso = 1

            i = 0

            while i <= len(camino_tiempo)-2:
                arista = G_tiempo.obtener_arista(
                    camino_tiempo[i], camino_tiempo[i+1])

                for aris in G_tiempo.aristas:
                    if aris.origen == camino_tiempo[i] and aris.destino == camino_tiempo[i+1]:
                        arista = aris

                # Es la primera, así que no tiene anterior -> entra solo si se encuentra en un vértice, ya que en el resto si tiene anterior
                if i == 0 and data_origen[1] == None:
                    tiempo_seguido += arista.peso
                    calle_anterior = arista

                elif i == len(camino_tiempo)-2:
                    if data_destino[1] == None:
                        cortes = ''
                        for corte in coordenadas[data_destino[0]]:
                            cortes += calles[corte][2] + ', '
                        string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(tiempo_seguido,2)} segundos. Hasta llegar al cruce de {cortes}'
                        paso += 1
                        string += f'\n{paso}. Vamos desde donde estamos hasta nuestro destino -> {round(data_destino[2],2)} segundos'
                    else:
                        if arista.data_arista['id'] == calle_anterior.data_arista["id"]:
                            tiempo_seguido += data_destino[2]
                            string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(tiempo_seguido,2)} segundos. Llegamos a nuestro destino'
                        else:
                            string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(tiempo_seguido,2)} segundos. Tomamos {angulo_calc(calle_anterior.origen, calle_anterior.destino, arista.destino)} {calles[arista.data_arista["id"]][2]}'
                            paso += 1
                            string += f'\n{paso}. Vamos por {calles[arista.data_arista["id"]][2]} -> {round(data_destino[2],2)} segundos. Llegamos a nuestro destino'
                else:
                    if arista.data_arista['id'] == calle_anterior.data_arista["id"]:
                        tiempo_seguido += arista.peso
                    else:
                        string += f'\n{paso}. Vamos por {calles[calle_anterior.data_arista["id"]][2]} -> {round(tiempo_seguido,2)} segundos. Tomamos {angulo_calc(calle_anterior.origen, calle_anterior.destino, arista.destino)} {calles[arista.data_arista["id"]][2]}'
                        paso += 1
                        tiempo_seguido = arista.peso
                        calle_anterior = arista

                i += 1

    print(string)

    if tipo == 1:
        print(
            f'\nLa distancia total es de {round(distancia_total + data_origen[2] + data_destino[2],2)} metros')
        return camino_dist
    else:
        print(
            f'\nEl tiempo total es de {round(tiempo_total + data_origen[2] + data_destino[2],2)} segundos')
        return camino_tiempo


def dibujar_camino(camino, data_origen, data_destino, tipo):

    # Convertimos el grafo a nx
    print("A continuación, se visualizará el grafo y el camino. En verde, se resalta el origen y en rojo el destino")
    if tipo == 1:
        G = G_dist.convertir_a_NetworkX()
        pos = posiciones_mapa_dist
    else:
        G = G_tiempo.convertir_a_NetworkX()
        pos = posiciones_mapa_tiempo

    # Añadimos vertice y aristas de origen y destino

    G.add_node(data_origen[3])
    G.add_node(data_destino[3])
    G.add_edge(data_origen[0], data_origen[3],
               object=None, weight=data_origen[2])
    G.add_edge(data_destino[0], data_destino[3],
               object=None, weight=data_destino[2])

    pos[data_origen[3]] = data_origen[3]
    pos[data_destino[3]] = data_destino[3]

    plot = plt.plot()

    camino_aristas = [(
        camino[i], camino[i+1]) for i in range(len(camino)-1)]

    camino_aristas.insert(0, (data_origen[3], camino[0]))
    camino_aristas.append((camino[-1], data_destino[3]))

    nx.draw(G, with_labels=False, pos=pos,
            edge_color='b', width=0.2, node_size=1)
    nx.draw_networkx_edges(
        G, pos=pos, edgelist=camino_aristas, edge_color='r', width=2)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=camino,
                           node_color='red', node_size=2)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=[
                           data_origen[3]], node_color='lime', node_size=2, label='Origen')
    nx.draw_networkx_nodes(G, pos=pos, nodelist=[
                           data_destino[3]], node_color='black', node_size=2, label='Destino')
    plt.show()

    G.remove_node(data_origen[3])
    G.remove_node(data_destino[3])

    del pos[data_origen[3]]
    del pos[data_destino[3]]


if __name__ == "__main__":

    salir = False

    cruces = pd.read_csv('cruces.csv', encoding='latin-1',
                         sep=';', low_memory=False)
    direcciones = pd.read_csv('direcciones.csv', encoding='latin-1',
                              sep=';', low_memory=False, dtype={'Literal de numeracion': str})

    G_dist = gf.Grafo(dirigido=False)
    G_tiempo = gf.Grafo(dirigido=False)

    vias = {'AUTOVIA': 100, 'AVENIDA': 90, 'CARRETERA': 70, 'CALLEJON': 30,
            'CAMINO': 30, 'ESTACIONDEMETRO': 20, 'PASADIZO': 20, 'PLAZUELA': 20, 'COLONIA': 20}

    coordenadas = {}     # {Coordenadas: [nombres vias]}
    calles = {}     # {Calle : [coordenadas de cruces, tipo, nombre]}
    posiciones_mapa_dist = {}    # {Vertice: [coordenadas de cruces]}
    posiciones_mapa_tiempo = {}    # {Vertice: [coordenadas de cruces]}
    codigos_calles = {}     # {Calle : [codigo]}

    crear_grafos()

    while not salir:

        salir, tipo = menu()

        if not salir:
            # Ahora preguntamos origen y destino
            salir, data_origen, data_destino = origen_destino(tipo)

            if not salir:

                # Ahora se saca el camino. Nos guardamos el camino para mostrarlo en el mapa

                camino = mostrar_camino(data_origen, data_destino, tipo)

                if camino != None:
                    dibujar_camino(camino, data_origen, data_destino, tipo)

                print('\n'*5)
