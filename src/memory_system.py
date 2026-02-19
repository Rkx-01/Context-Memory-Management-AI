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
            self.nodes[source_id].add_edge(target_id, relationship)
            self.nodes[target_id].add_edge(source_id, f"REVERSE_{relationship}")

    def _calculate_temporal_proximity(self, node: MemoryNode, current_time: datetime.datetime) -> float:
        """Calculates Proximity Score decay based on age."""
        if node.is_evergreen:
            return 1.0
        
        age_days = (current_time - node.timestamp).days
        if age_days < 0:
            age_days = 0
            
        # Exponential decay: P_temp = e^(-λt)
        decay_score = math.exp(-self._lambda * age_days)
        return max(0.01, decay_score) # Don't drop all the way to 0

    def _calculate_relational_distance(self, start_id: str, target_id: str, max_depth: int = 3) -> float:
        """Calculates graph distance using BFS. Shorter distance = higher score."""
        if start_id == target_id:
            return 1.0
        
        queue = [(start_id, 0)]
        visited = {start_id}
        
        while queue:
            curr_id, depth = queue.pop(0)
            
            if curr_id == target_id:
                # Degree 1 = 1.0, Degree 2 = 0.5, Degree 3 = 0.33
                return 1.0 / depth
                
            if depth < max_depth:
                current_node = self.nodes.get(curr_id)
