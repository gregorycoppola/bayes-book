# app/models/bayesnet.py
from typing import List, Dict, Optional
from pydantic import BaseModel


class CPTEntry(BaseModel):
    parent_values: Dict[str, str]
    probability: float


class VariableNode(BaseModel):
    name: str
    domain: List[str]
    parents: List[str] = []
    cpt: Dict[str, List[CPTEntry]]


class BayesianNetwork(BaseModel):
    name: Optional[str] = None
    nodes: List[VariableNode]
