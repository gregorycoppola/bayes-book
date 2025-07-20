# app/storage/in_memory.py
import json
import redis.asyncio as redis
from app.models.bayesnet import BayesianNetwork

# Connect to Redis (localhost by default)
_redis = redis.Redis(host="localhost", port=6379, decode_responses=True)

NAMESPACE = "bayesnet:"


async def save_network(name: str, network: BayesianNetwork):
    key = f"{NAMESPACE}{name}"
    data = network.json()
    await _redis.set(key, data)


async def get_network(name: str) -> BayesianNetwork:
    key = f"{NAMESPACE}{name}"
    data = await _redis.get(key)
    if not data:
        raise KeyError(f"Network '{name}' not found in Redis")
    return BayesianNetwork.parse_raw(data)


async def list_networks() -> list[str]:
    keys = await _redis.keys(f"{NAMESPACE}*")
    return [key.removeprefix(NAMESPACE) for key in keys]
