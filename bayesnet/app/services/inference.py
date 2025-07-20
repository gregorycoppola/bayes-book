# app/services/inference.py
from app.models.bayesnet import BayesianNetwork
from collections import defaultdict
from typing import Dict, List


def query(network: BayesianNetwork, evidence: dict, query_var: str) -> dict:
    """
    Stub function for querying a Bayesian Network.
    For now, just returns the query request info.
    """
    return {
        "query_variable": query_var,
        "evidence": evidence,
        "message": "Inference engine not implemented yet."
    }



def compute_beliefs_loopy_bp(
    network: BayesianNetwork,
    evidence: Dict[str, str],
    iterations: int = 10
) -> Dict[str, Dict[str, float]]:
    node_map = {node.name: node for node in network.nodes}
    neighbors = build_neighbor_map(network)

    # Initialize messages to uniform distributions
    messages = defaultdict(lambda: defaultdict(dict))
    for node in network.nodes:
        for neighbor in neighbors[node.name]:
            for val in node.domain:
                messages[node.name][neighbor][val] = 1.0

    # Iteratively update messages
    for _ in range(iterations):
        new_messages = defaultdict(lambda: defaultdict(dict))
        for i in node_map:
            for j in neighbors[i]:
                new_messages[i][j] = compute_message(i, j, messages, node_map, evidence)

        messages = new_messages  # update messages

    # Compute beliefs
    beliefs = {}
    for var in node_map:
        if var in evidence:
            beliefs[var] = {evidence[var]: 1.0}
        else:
            incoming = neighbors[var]
            domain = node_map[var].domain
            unnormalized = {val: 1.0 for val in domain}
            for val in domain:
                for neighbor in incoming:
                    unnormalized[val] *= messages[neighbor][var].get(val, 1.0)

                # Multiply by local CPT if no parents (prior)
                if not node_map[var].parents:
                    unnormalized[val] *= get_prior(var, val, node_map)

            beliefs[var] = normalize(unnormalized)

    return beliefs


def build_neighbor_map(network: BayesianNetwork) -> Dict[str, List[str]]:
    neighbors = defaultdict(set)
    for node in network.nodes:
        for parent in node.parents:
            neighbors[node.name].add(parent)
            neighbors[parent].add(node.name)
    return {k: list(v) for k, v in neighbors.items()}


def compute_message(
    from_node: str,
    to_node: str,
    messages: Dict[str, Dict[str, Dict[str, float]]],
    node_map: Dict[str, VariableNode],
    evidence: Dict[str, str]
) -> Dict[str, float]:
    node = node_map[from_node]
    if from_node in evidence:
        return {val: 1.0 if val == evidence[from_node] else 0.0 for val in node.domain}

    result = {}
    for x in node.domain:
        product = 1.0
        for neighbor in messages[from_node]:
            if neighbor == to_node:
                continue
            product *= messages[neighbor][from_node].get(x, 1.0)
        result[x] = product

    return normalize(result)


def normalize(distribution: Dict[str, float]) -> Dict[str, float]:
    total = sum(distribution.values())
    if total == 0:
        return {k: 1.0 / len(distribution) for k in distribution}
    return {k: v / total for k, v in distribution.items()}


def get_prior(var: str, value: str, node_map: Dict[str, VariableNode]) -> float:
    node = node_map[var]
    entries = node.cpt[value]
    for entry in entries:
        if entry.parent_values == {}:
            return entry.probability
    raise ValueError(f"Missing prior for {var}={value}")
