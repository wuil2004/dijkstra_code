let svg = d3.select("#graph");
let width = +svg.attr("width");
let height = +svg.attr("height");
let simulation, link, node, label;

function dibujarGrafo(data) {
    svg.selectAll("*").remove();

    simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
        .force("charge", d3.forceManyBody().strength(-400))
        .force("center", d3.forceCenter(width / 2, height / 2));

    link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(data.links)
        .join("line")
        .attr("stroke-width", 2)
        .attr("class", d => esAristaEnCamino(d, data.pathEdges) ? "link highlight" : "link");

    node = svg.append("g")
        .selectAll("circle")
        .data(data.nodes)
        .join("circle")
        .attr("r", 15)
        .attr("fill", "lightblue")
        .attr("stroke", "#333")
        .attr("stroke-width", 1.5)
        .call(drag(simulation));

    label = svg.append("g")
        .selectAll("text")
        .data(data.nodes)
        .join("text")
        .text(d => d.id)
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
        .attr("dy", 4);

    // Agregar etiquetas con los pesos de las aristas
    let edgeLabels = svg.append("g")
        .selectAll("text")
        .data(data.links)
        .join("text")
        .attr("font-size", 12)
        .attr("fill", "black")
        .attr("text-anchor", "middle")
        .text(d => d.weight);

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);

        label
            .attr("x", d => d.x)
            .attr("y", d => d.y);

        edgeLabels
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);
    });
}

function esAristaEnCamino(arista, pathEdges) {
    return pathEdges.some(p =>
        (p.source === arista.source.id && p.target === arista.target.id) ||
        (p.source === arista.target.id && p.target === arista.source.id)
    );
}

function drag(simulation) {
    return d3.drag()
        .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        })
        .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        })
        .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        });
}

document.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault(); // Evita recarga

    const form = e.target;
    const datos = new FormData(form);

    fetch("/resolver", {
        method: "POST",
        body: datos,
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
        .then(r => r.json())
        .then(data => {
            // Mostrar resultado en texto
            document.querySelector("p.camino")?.remove();
            document.querySelector("p.distancia")?.remove();

            const resultado = document.querySelector("h2 + p")?.parentNode || form;

            let caminoP = document.createElement("p");
            caminoP.className = "camino";
            caminoP.innerHTML = `<strong>Camino:</strong> ${data.camino.join(" → ")}`;
            resultado.appendChild(caminoP);

            let distanciaP = document.createElement("p");
            distanciaP.className = "distancia";
            distanciaP.innerHTML = `<strong>Distancia total:</strong> ${data.distancia}`;
            resultado.appendChild(distanciaP);

            // Dibujar grafo
            dibujarGrafo({
                nodes: data.nodes,
                links: data.links,
                pathEdges: data.path_edges
            });
        });
});
