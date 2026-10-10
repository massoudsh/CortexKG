import networkx as nx
from models import KnowledgeGraph

def initialize_graph() -> nx.DiGraph:
    """Creates a new empty directed graph."""
    return nx.DiGraph()


def sample_knowledge_graph() -> KnowledgeGraph:
    """Returns a representative, evidence-oriented project graph."""
    return KnowledgeGraph(
        nodes=[
            {"id": "maya", "label": "Maya", "entity_type": "Person"},
            {"id": "omar", "label": "Omar", "entity_type": "Person"},
            {"id": "project-atlas", "label": "Project Atlas", "entity_type": "Project"},
            {"id": "api-migration", "label": "API Migration", "entity_type": "Initiative"},
            {"id": "postgresql", "label": "PostgreSQL", "entity_type": "Technology"},
            {"id": "token-retention-risk", "label": "Token retention risk", "entity_type": "Risk"},
            {"id": "november-launch", "label": "November launch", "entity_type": "Milestone"},
        ],
        edges=[
            {"source": "maya", "target": "api-migration", "relation": "owns"},
            {"source": "api-migration", "target": "project-atlas", "relation": "supports"},
            {"source": "project-atlas", "target": "postgresql", "relation": "uses"},
            {"source": "omar", "target": "token-retention-risk", "relation": "identified"},
            {"source": "omar", "target": "api-migration", "relation": "reviews"},
            {"source": "token-retention-risk", "target": "november-launch", "relation": "must resolve before"},
        ],
    )

def update_graph(nx_graph: nx.DiGraph, kg: KnowledgeGraph) -> nx.DiGraph:
    """Idempotently adds new nodes and edges to the NetworkX graph."""
    for node in kg.nodes:
        nx_graph.add_node(
            node.id, 
            label=node.label, 
            title=f"Type: {node.entity_type}",
            shape="dot",
            size=20
        )
        
    for edge in kg.edges:
        # Prevent floating edges by validating both source and target exist
        if edge.source in nx_graph.nodes and edge.target in nx_graph.nodes:
            nx_graph.add_edge(
                edge.source, 
                edge.target, 
                label=edge.relation,
                title=edge.relation
            )
            
    return nx_graph