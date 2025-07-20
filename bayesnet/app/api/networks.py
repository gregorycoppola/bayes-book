# app/api/networks.py
from fastapi import APIRouter
from app.models.bayesnet import BayesianNetwork

router = APIRouter()

@router.post("/")
async def upload_network(network: BayesianNetwork):
    return {
        "message": f"Received network '{network.name or 'unnamed'}'",
        "node_count": len(network.nodes)
    }
