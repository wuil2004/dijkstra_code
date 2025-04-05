import heapq
import networkx as nx
import matplotlib.pyplot as plt

def mostrar_grafo(grafo_nx, camino_resaltado=None):
    plt.clf()
    pos = nx.spring_layout(grafo_nx)

    edge_colors = []
    edge_widths = []

    if camino_resaltado:
        edges_resaltados = set(zip(camino_resaltado, camino_resaltado[1:]))
    else:
        edges_resaltados = set()

    for u, v in grafo_nx.edges():
        if (u, v) in edges_resaltados:
            edge_colors.append('red')
            edge_widths.append(2.5)
        else:
            edge_colors.append('gray')
            edge_widths.append(1)

    nx.draw(
        grafo_nx, pos, with_labels=True, node_color='skyblue',
        node_size=1500, font_size=10, edge_color=edge_colors, width=edge_widths
    )

    etiquetas = nx.get_edge_attributes(grafo_nx, 'weight')
    nx.draw_networkx_edge_labels(grafo_nx, pos, edge_labels=etiquetas)
    plt.pause(0.5)

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    padres = {nodo: None for nodo in grafo}
    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        for vecino, peso in grafo[nodo_actual]:
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                padres[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia, vecino))

    return distancias, padres

def construir_camino(padres, destino):
    camino = []
    while destino is not None:
        camino.append(destino)
        destino = padres[destino]
    return camino[::-1]

def main():
    grafo = {}

    dirigido_input = input("¿El grafo es dirigido (con flechas)? (s/n): ").strip().lower()
    es_dirigido = True if dirigido_input == 's' else False
    grafo_nx = nx.DiGraph() if es_dirigido else nx.Graph()

    plt.ion()

    n = int(input("¿Cuántos nodos tiene el grafo? "))
    for i in range(n):
        nodo = input(f"Nombre del nodo {i + 1}: ")
        grafo[nodo] = []
        grafo_nx.add_node(nodo)

    print("\nAhora ingresa las conexiones (aristas). Escribe 'fin' para terminar.")
    while True:
        origen = input("Nodo de origen (o 'fin'): ")
        if origen.lower() == 'fin':
            break
        destino = input("Nodo de destino: ")
        peso = int(input(f"Peso de la arista de {origen} a {destino}: "))

        grafo[origen].append((destino, peso))
        grafo_nx.add_edge(origen, destino, weight=peso)

        if not es_dirigido:
            grafo[destino].append((origen, peso))  # Grafo no dirigido
            grafo_nx.add_edge(destino, origen, weight=peso)

        mostrar_grafo(grafo_nx)

    inicio = input("\n¿Desde qué nodo quieres calcular el camino más corto? ")
    destino_final = input("¿Hasta qué nodo quieres llegar?: ")

    distancias, padres = dijkstra(grafo, inicio)
    camino = construir_camino(padres, destino_final)

    print(f"\nDistancia más corta desde {inicio} hasta {destino_final}: {distancias[destino_final]}")
    print("Camino más corto:", " -> ".join(camino))

    plt.ioff()
    mostrar_grafo(grafo_nx, camino_resaltado=camino)
    plt.show()

if __name__ == "__main__":
    main()
