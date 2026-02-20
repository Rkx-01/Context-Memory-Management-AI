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
                if current_node:
                    for neighbor_id in current_node.edges:
                        if neighbor_id not in visited:
                            visited.add(neighbor_id)
                            queue.append((neighbor_id, depth + 1))
                            
        return 0.0 # No relationship within max_depth

    def _mock_semantic_similarity(self, query: str, node_content: str) -> float:
        """Mocks a vector embedding cosine similarity score."""
        query_words = set(query.lower().split())
        content_words = set(node_content.lower().split())
        
        if not query_words or not content_words:
            return 0.0
            
        intersection = query_words.intersection(content_words)
        return len(intersection) / max(len(query_words), 1)

    def retrieve_context(self, current_interaction: 'MemoryNode', current_time: datetime.datetime, 
                         query: str = "", top_k: int = 5) -> List[tuple[MemoryNode, float]]:
        """
        Retrieves and ranks historical context based on Proximity Scoring.
        Returns a sorted list of (Node, Score).
        """
        results = []
        
        for n_id, node in self.nodes.items():
            if n_id == current_interaction.node_id:
                continue
                
            # 1. Temporal
            p_temp = self._calculate_temporal_proximity(node, current_time)
            
            # 2. Relational (Graph Distance from current interaction)
            # Find closest connected entity (e.g., this invoice -> connected to what supplier -> connected to past issues)
            # Find the core entity this interaction is about to serve as the start of the graph search
            p_rel = 0.0
            for edge_target in current_interaction.edges:
                dist = self._calculate_relational_distance(edge_target, n_id)
                if dist > p_rel:
                    p_rel = dist

            # 3. Semantic
            p_sem = self._mock_semantic_similarity(query, node.content) if query else 1.0
            
            # Final Proximity Score
            score = (self.w_temp * p_temp + self.w_rel * p_rel + self.w_sem * p_sem) * node.importance
            
            # Only include if there is *some* relevance (relational or semantic match)
            if p_rel > 0 or p_sem > 0.2:
                results.append((node, score))
                
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
