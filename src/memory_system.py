import datetime
import math
from typing import List, Dict, Any, Optional

class MemoryNode:
    """Represents a discrete memory or entity in the Knowledge Graph Context."""
    def __init__(self, node_id: str, node_type: str, content: str, 
                 timestamp: datetime.datetime, 
                 is_evergreen: bool = False,
                 importance: float = 1.0):
        self.node_id = node_id
        self.node_type = node_type  # e.g., 'Supplier', 'Invoice', 'Issue', 'Ticket', 'Customer'
        self.content = content
        self.timestamp = timestamp
        self.is_evergreen = is_evergreen # If True, lambda decay is 0
        self.importance = importance # Base multiplier
        self.edges: Dict[str, str] = {} # target_node_id -> relationship_type

    def add_edge(self, target_node_id: str, relationship: str):
        self.edges[target_node_id] = relationship

    def __repr__(self):
        return f"[{self.node_type}] {self.content}"

class MemoryManager:
    """Manages the lifecycle, ranking, and retrieval of memory nodes."""
    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}
        # Tunable parameters for the proximity score equation
        self.w_temp = 1.0
        self.w_rel = 1.0
        self.w_sem = 1.0
        
        # Decay half-life (in days) for time-sensitive info
        self.half_life_days = 90.0
        self._lambda = math.log(2) / self.half_life_days

    def add_node(self, node: MemoryNode):
        self.nodes[node.node_id] = node

    def link_nodes(self, source_id: str, target_id: str, relationship: str):
        """Creates a bidirectional edge between two concepts."""
        if source_id in self.nodes and target_id in self.nodes:
