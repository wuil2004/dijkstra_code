from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dijkstra import dijkstra, construir_camino

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

    return templates.TemplateResponse("index.html", {
        "request": request,
        "camino": camino,
        "distancia": distancia,
        "origen": origen,
        "destino": destino
    })
