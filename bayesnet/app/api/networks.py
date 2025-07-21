# app/api/networks.py
from fastapi import APIRouter, HTTPException, Body
from app.models.bayesnet import BayesianNetwork
from app.storage.in_memory import save_network, get_network, list_networks
from app.services.inference import compute_beliefs_loopy_bp

router = APIRouter()


@router.post("/{name}")
async def upload_network(name: str, network: BayesianNetwork):
    await save_network(name, network)
    return {
        "message": f"Stored network '{name}'",
        "node_count": len(network.nodes)
    }


@router.get("/{name}")
async def get_network_by_name(name: str):
    try:
        network = await get_network(name)
        return network
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Network '{name}' not found")


@router.get("/")
async def list_all_networks():
    names = await list_networks()
    return {"networks": names}

@router.post("/{name}/infer")
async def infer_network(name: str, payload: dict = Body(...)):
    try:
        network = await get_network(name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Network '{name}' not found")

    evidence = payload.get("evidence", {})
    iterations = payload.get("iterations", 10)

    result = compute_beliefs_loopy_bp(network, evidence, iterations)
    return result

@router.get("/{name}/graph")
async def get_network_graph(name: str):
    try:
        network = await get_network(name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Network '{name}' not found")

    nodes = [{"id": node.name, "label": node.name} for node in network.nodes]
    edges = []
    for node in network.nodes:
        for parent in node.parents:
            edges.append({"from": parent, "to": node.name})

    return {"nodes": nodes, "edges": edges}
