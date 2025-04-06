from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dijkstra import dijkstra, construir_camino
import networkx as nx
import matplotlib.pyplot as plt
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/resolver", response_class=HTMLResponse)
async def resolver(request: Request,
                nodos: str = Form(...),
                aristas: str = Form(...),
                origen: str = Form(...),
                destino: str = Form(...),
                dirigido: str = Form("no")):

    nodos = nodos.replace(" ", "").split(",")
    grafo = {n: [] for n in nodos}
    dirigido = dirigido == "si"

    for arista in aristas.strip().split("\n"):
        u, v, peso = arista.strip().split(",")
        peso = int(peso)
        grafo[u].append((v, peso))
        if not dirigido:
            grafo[v].append((u, peso))

    distancias, padres = dijkstra(grafo, origen)
    camino = construir_camino(padres, destino)
    distancia = distancias[destino]

    dibujar_grafo(grafo, camino)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "camino": camino,
        "distancia": distancia,
        "origen": origen,
        "destino": destino
    })

def dibujar_grafo(grafo, camino=None, nombre_archivo="static/grafo.png"):
    G = nx.DiGraph() if any(isinstance(v, list) for v in grafo.values()) else nx.Graph()
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_labels(G, pos)

    edge_colors = []
    for u, v in G.edges():
        if camino and (u, v) in zip(camino, camino[1:]):
            edge_colors.append('red')
        else:
            edge_colors.append('gray')

    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(nombre_archivo)
    plt.close()
