import queue

import queue

import queue

import queue

import queue

def buscar_camino(matriz):
    # Encuentra la posición de Coraje (1) y Muriel (2)
    fila_coraje, columna_coraje = encontrar_personaje(matriz, 1)
    fila_muriel, columna_muriel = encontrar_personaje(matriz, 2)

    if fila_coraje is None or columna_coraje is None or fila_muriel is None or columna_muriel is None:
        print("No se encontró a Coraje o a Muriel en la matriz.")
        return None

    # Define una cola de prioridad para almacenar los nodos a explorar
    start = (fila_coraje, columna_coraje)
    frontier = queue.PriorityQueue()
    frontier.put((0, start))  # Incluye el costo acumulado en la cola de prioridad

    # Un diccionario para realizar un seguimiento de los nodos padres y costos acumulados
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        _, current = frontier.get()  # Obtiene el nodo con el costo acumulado más bajo

        if current == (fila_muriel, columna_muriel):
            # Reconstruye y regresa el camino encontrado
            path = []
            while current is not None:
                path.insert(0, current)
                current = came_from[current]

            print("Camino encontrado:")
            for paso in path:
                print(f"->{paso}", end=" ")
            print("\nNodos generados:")
            for nodo_generado in came_from:
                costo_acumulado = cost_so_far.get(nodo_generado, "N/A")
                costo_real = costo_acumulado - (cost_so_far[came_from[nodo_generado]] if came_from[nodo_generado] else 0)
                print(f"Nodo: {nodo_generado}, Costo Real: {costo_real}, Costo Acumulado: {costo_acumulado}")

            return path

        for next, costo in obtener_vecinos(current, matriz):
            new_cost = cost_so_far[current] + costo
            if next not in cost_so_far or new_cost < cost_so_far.get(next, float('inf')):
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put((new_cost, next))  # Incluye el nuevo costo acumulado en la cola de prioridad
                came_from[next] = current

    print("No se encontró un camino.")
    return None





def encontrar_personaje(matriz, personaje):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            if matriz[fila][columna] == personaje:
                return fila, columna
    return None, None

def obtener_vecinos(pos, matriz):
    fila, columna = pos
    vecinos = []

    # Movimientos arriba, abajo, izquierda, derecha
    movimientos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]

    for fila_nueva, columna_nueva in movimientos:
        if 0 <= fila_nueva < len(matriz) and 0 <= columna_nueva < len(matriz[0]):
            if matriz[fila_nueva][columna_nueva] == 6:
                continue  # Evitar las paredes

            if matriz[fila_nueva][columna_nueva] == 3:
                costo = 3  # Costo de pasar por un gato
            else:
                costo = 1  # Costo uniforme

            vecinos.append(((fila_nueva, columna_nueva), costo))

    return vecinos
