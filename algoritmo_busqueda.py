import queue
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

def buscar_camino(matriz):
    fila_coraje, columna_coraje = encontrar_personaje(matriz, 1)
    fila_muriel, columna_muriel = encontrar_personaje(matriz, 2)

    start = (fila_coraje, columna_coraje)
    frontier = queue.PriorityQueue()
    frontier.put((0, start))

    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    nodos = {}
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            nodos[(fila, columna)] = Node((fila, columna))

    root = nodos[start]

    previous_node = None
    

    while not frontier.empty():
        _, current = frontier.get()

        if current == (fila_muriel, columna_muriel):
            path = []
            cost = []
            total_cost = cost_so_far[current]
            while current is not None:
                print(cost_so_far[current])
                path.insert(0, current)

                current = came_from[current]
            
            print("Camino encontrado:")
            for paso in path:
                print(f"->{paso}", end=" ")
            print("\nNodos generados:")

            for nodo_generado in came_from:
                costo_acumulado = cost_so_far.get(nodo_generado, "N/A")
                costo_real = costo_acumulado - (cost_so_far[came_from[nodo_generado]] if came_from[nodo_generado] else 0)
                
                nodo_actual = nodos[nodo_generado]
                nodo_actual.costo_acumulado = costo_acumulado
                nodo_actual.costo_real = costo_real
                
                nodo_padre = nodos[came_from[nodo_generado]] if came_from[nodo_generado] is not None else None
                nodo_actual.parent = nodo_padre
                
                nodo_actual.name = f"{nodo_generado} CR: {costo_real} CA: {costo_acumulado}"
            
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.name))

            for asd in path:
                costo_acumulado = cost_so_far.get(asd)
                cost.insert(0, costo_acumulado)
            
            print(cost)
            return path, cost

        
        vecinos = obtener_vecinos(current, matriz)
        anterior = came_from[current]
        vecinos = [(pos, costo) for pos, costo in vecinos if pos != anterior]
        

        # Guarda los costos acumulados de los vecinos para determinar el más bajo
        vecino_costos = []
        for next, costo in vecinos:
        
            new_cost = cost_so_far[current] + costo
            vecino_costos.append(new_cost)
            

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                #previous_node = came_from[next]
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put((new_cost, next))
                came_from[next] = current
            
                

        if previous_node:
            vecinos_previos = obtener_vecinos(previous_node, matriz)
            vecinos_posiciones = [vecino[0] for vecino in vecinos_previos]
            if current not in vecinos_posiciones:
               # print(f"Cambiando de rama de {previous_node} a {current}")

                last = came_from[previous_node]
                previous_vecinos = obtener_vecinos(previous_node, matriz)
                previous_vecinos = [(pos, costo) for pos, costo in previous_vecinos if pos != last]

                if previous_vecinos:
                    hijo_min_costo = min(previous_vecinos, key=lambda x: x[1])
                    coord_hijo_min_costo, costo_min = hijo_min_costo
                    #print(hijo_min_costo)
                    cost_so_far[previous_node] = cost_so_far[coord_hijo_min_costo]

        if current == (4,6):
            print(cost_so_far, "aqui es")        
        previous_node = current 
        #print(current, "este es el actual de la rama")


    print("No se encontró un camino.")
    return None







def encontrar_personaje(matriz, personaje):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            if matriz[fila][columna] == personaje:
                return fila, columna
    return None, None


def encontrar_amo_malvado(matriz):
    ubicaciones = []  # Una lista para almacenar las ubicaciones de los amo malvados

    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            if matriz[fila][columna] == 4:  # Comprueba si el elemento en la matriz es un "amo malvado" (valor 4)
                ubicaciones.append((fila, columna))  # Agrega la ubicación a la lista
    return ubicaciones

def obtener_vecinos(pos, matriz):
    fila, columna = pos
    vecinos = []

    # Movimientos arriba, abajo, izquierda, derecha
    movimientos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]

    for fila_nueva, columna_nueva in movimientos:
        if 0 <= fila_nueva < len(matriz) and 0 <= columna_nueva < len(matriz[0]):
            if matriz[fila_nueva][columna_nueva] == 6:
                continue

            if matriz[fila_nueva][columna_nueva] == 4:
                costo = -2
            elif matriz[fila_nueva][columna_nueva] == 3:
                costo = 3
            else:
                costo = 1
            
            vecinos.append(((fila_nueva, columna_nueva), costo))
           

    return vecinos
