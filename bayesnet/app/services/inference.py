# app/services/inference.py
from app.models.bayesnet import BayesianNetwork


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
