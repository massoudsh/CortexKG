import networkx as nx
from models import KnowledgeGraph

def initialize_graph() -> nx.DiGraph:
    """Creates a new empty directed graph."""
    return nx.DiGraph()


def graph_statistics(graph: nx.DiGraph) -> dict[str, int]:
    """Returns graph totals grouped by optional review status."""
    confirmed_memories = sum(
        1 for _, data in graph.nodes(data=True)
        if data.get("review_status") == "confirmed"
    )
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "confirmed_memories": confirmed_memories,
        "unreviewed_memories": graph.number_of_nodes() - confirmed_memories,
    }


def format_graph_statistics(graph: nx.DiGraph) -> str:
    """Formats graph statistics for sharing or copying."""
    statistics = graph_statistics(graph)
    return "\n".join([
        "CortexKG Statistics",
        "",
        f"Nodes: {statistics['nodes']}",
        f"Edges: {statistics['edges']}",
        f"Confirmed Memories: {statistics['confirmed_memories']}",
        f"Unreviewed Memories: {statistics['unreviewed_memories']}",
    ])


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