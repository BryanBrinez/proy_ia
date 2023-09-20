import queue

# Función para encontrar el camino utilizando búsqueda de costo uniforme
def buscar_camino(matriz):
    # Encuentra la posición del destino y del personaje en la matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 4:
                fila_destino = i
                columna_destino = j
            elif matriz[i][j] == 3:
                fila_inicio = i
                columna_inicio = j
    
    # Cola de prioridad para explorar nodos
    cola_prioridad = queue.PriorityQueue()
    
    # Nodo inicial (fila, columna, costo, camino)
    nodo_inicial = (fila_inicio, columna_inicio, 0, [(fila_inicio, columna_inicio)])  # Incluimos la posición inicial en el camino
    cola_prioridad.put(nodo_inicial)
    
    # Direcciones posibles de movimiento (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Diccionario para rastrear los costos mínimos
    costos_minimos = {(i, j): float('inf') for i in range(len(matriz)) for j in range(len(matriz[0]))}
    costos_minimos[(fila_inicio, columna_inicio)] = 0
    
    while not cola_prioridad.empty():
        fila_actual, columna_actual, costo_actual, camino_actual = cola_prioridad.get()
        
        if fila_actual == fila_destino and columna_actual == columna_destino:
            # Llegamos al destino, retornamos el camino
            return camino_actual
        
        for direccion in direcciones:
            fila_nueva = fila_actual + direccion[0]
            columna_nueva = columna_actual + direccion[1]
            
            if (
                0 <= fila_nueva < len(matriz) and
                0 <= columna_nueva < len(matriz[0]) and
                (matriz[fila_nueva][columna_nueva] == 0 or
                 matriz[fila_nueva][columna_nueva] == 4) and
                costo_actual + 1 < costos_minimos[(fila_nueva, columna_nueva)]
            ):
                # Movimiento válido, agregamos el nuevo nodo a la cola con costo actualizado
                nuevo_costo = costo_actual + 1
                nuevo_camino = camino_actual + [(fila_nueva, columna_nueva)]
                cola_prioridad.put((fila_nueva, columna_nueva, nuevo_costo, nuevo_camino))
                costos_minimos[(fila_nueva, columna_nueva)] = nuevo_costo
    
    # No se encontró un camino válido
    return None
