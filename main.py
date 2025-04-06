from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Grafo:
    def __init__(self):
        self.adyacencia = {}

    def agregar_nodo(self, nodo):
        if nodo not in self.adyacencia:
            self.adyacencia[nodo] = []

    def agregar_arista(self, origen, destino, peso, dirigido):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.adyacencia[origen].append((destino, peso))
        if not dirigido:
            self.adyacencia[destino].append((origen, peso))

    def dijkstra(self, inicio, fin):
        import heapq
        distancias = {nodo: float("inf") for nodo in self.adyacencia}
        anterior = {nodo: None for nodo in self.adyacencia}
        distancias[inicio] = 0
        cola = [(0, inicio)]

        while cola:
            dist_actual, nodo_actual = heapq.heappop(cola)

            if nodo_actual == fin:
                break

            for vecino, peso in self.adyacencia[nodo_actual]:
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    anterior[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_dist, vecino))

        camino = []
        actual = fin
        while actual:
            camino.insert(0, actual)
            actual = anterior[actual]
        if distancias[fin] == float("inf"):
            camino = []

        return camino, distancias[fin]

    def obtener_nodos_y_aristas(self):
        nodos = [{"id": nodo} for nodo in self.adyacencia]
        aristas = []
        for origen, destinos in self.adyacencia.items():
            for destino, peso in destinos:
                aristas.append({"source": origen, "target": destino, "weight": peso})
        return nodos, aristas

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resolver", methods=["POST"])
def resolver():
    nodos = request.form["nodos"].split(",")
    aristas_texto = request.form["aristas"].strip().split("\n")
    dirigido = request.form["dirigido"] == "si"
    origen = request.form["origen"]
    destino = request.form["destino"]

    grafo = Grafo()
    for nodo in nodos:
        grafo.agregar_nodo(nodo.strip())

    for linea in aristas_texto:
        partes = linea.strip().split(",")
        if len(partes) == 3:
            n1, n2, peso = partes
            grafo.agregar_arista(n1.strip(), n2.strip(), int(peso), dirigido)

    camino, distancia = grafo.dijkstra(origen, destino)

    nodes, links = grafo.obtener_nodos_y_aristas()
    path_edges = [
        {"source": camino[i], "target": camino[i + 1]}
        for i in range(len(camino) - 1)
    ]

    # Si la petición viene desde JavaScript (AJAX), devolvemos JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "camino": camino,
            "distancia": distancia,
            "nodes": nodes,
            "links": links,
            "path_edges": path_edges
        })

    # Si no, devolvemos HTML tradicional
    return render_template(
        "index.html",
        camino=camino,
        distancia=distancia,
        nodes=nodes,
        links=links,
        path_edges=path_edges
    )

if __name__ == "__main__":
    app.run(debug=True)
