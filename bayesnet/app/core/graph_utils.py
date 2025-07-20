# app/core/graph_utils.py
from typing import List, Dict, Set


def is_dag(nodes: List[str], edges: Dict[str, List[str]]) -> bool:
    visited = set()
    visiting = set()

    def dfs(node: str) -> bool:
        if node in visited:
            return True
        if node in visiting:
            return False  # cycle detected
        visiting.add(node)
        for neighbor in edges.get(node, []):
            if not dfs(neighbor):
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    return all(dfs(n) for n in nodes if n not in visited)
