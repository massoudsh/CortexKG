import networkx as nx
from models import KnowledgeGraph


DEFAULT_MEMORY_STATUS = "unreviewed"


def initialize_graph() -> nx.DiGraph:
    """Creates a new empty directed graph."""
    return nx.DiGraph()


def graph_statistics(graph: nx.DiGraph) -> dict[str, int]:
    """Returns graph totals grouped by optional review status."""
    confirmed_memories = sum(
        1 for _, data in graph.nodes(data=True)
        if data.get("review_status") == "confirmed" or data.get("status") == "confirmed"
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


def ensure_memory_metadata(nx_graph: nx.DiGraph) -> nx.DiGraph:
    """
    Adds backward-compatible memory metadata to existing nodes.
    This allows older graph_memory.json files to work without migration.
    """
    for node_id, data in nx_graph.nodes(data=True):
        data.setdefault("label", str(node_id))
        data.setdefault("entity_type", "unknown")
        data.setdefault("status", DEFAULT_MEMORY_STATUS)

    return nx_graph


def update_graph(nx_graph: nx.DiGraph, kg: KnowledgeGraph) -> nx.DiGraph:
    """Idempotently adds new nodes and edges to the NetworkX graph."""

    ensure_memory_metadata(nx_graph)

    for node in kg.nodes:

        # Preserve existing memory status if the node already exists
        existing_data = nx_graph.nodes[node.id] if node.id in nx_graph.nodes else {}

        nx_graph.add_node(
            node.id,
            label=node.label,
            entity_type=node.entity_type,
            status=existing_data.get("status", DEFAULT_MEMORY_STATUS),
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


def update_memory_node(
    nx_graph: nx.DiGraph,
    node_id: str,
    label: str,
    entity_type: str
) -> nx.DiGraph:
    """Updates a memory node without changing its ID."""

    if node_id not in nx_graph.nodes:
        return nx_graph

    nx_graph.nodes[node_id]["label"] = label.strip()
    nx_graph.nodes[node_id]["entity_type"] = entity_type.strip()
    nx_graph.nodes[node_id]["title"] = f"Type: {entity_type}"

    return nx_graph


def set_memory_status(
    nx_graph: nx.DiGraph,
    node_id: str,
    status: str
) -> nx.DiGraph:
    """Sets memory status: confirmed, rejected, or unreviewed."""

    if node_id in nx_graph.nodes:
        nx_graph.nodes[node_id]["status"] = status

    return nx_graph


def delete_memory(
    nx_graph: nx.DiGraph,
    node_id: str
) -> nx.DiGraph:
    """Deletes a memory and all connected relationships."""

    if node_id in nx_graph.nodes:
        nx_graph.remove_node(node_id)

    return nx_graph


def get_memory_stats(nx_graph: nx.DiGraph) -> dict:
    """Returns high-level graph memory statistics."""

    ensure_memory_metadata(nx_graph)

    status_counts = {
        "confirmed": 0,
        "unreviewed": 0,
        "rejected": 0,
    }

    for _, data in nx_graph.nodes(data=True):
        status = data.get("status", DEFAULT_MEMORY_STATUS)

        if status not in status_counts:
            status_counts[status] = 0

        status_counts[status] += 1

    entity_types = {}

    for _, data in nx_graph.nodes(data=True):
        entity_type = data.get("entity_type", "unknown")
        entity_types[entity_type] = entity_types.get(entity_type, 0) + 1

    return {
        "nodes": len(nx_graph.nodes),
        "edges": len(nx_graph.edges),
        "confirmed": status_counts.get("confirmed", 0),
        "unreviewed": status_counts.get("unreviewed", 0),
        "rejected": status_counts.get("rejected", 0),
        "entity_types": entity_types,
    }


def get_memory_nodes(
    nx_graph: nx.DiGraph,
    search: str = "",
    entity_type: str = "All",
    status: str = "All"
) -> list[dict]:
    """Returns filtered memories for the UI."""

    ensure_memory_metadata(nx_graph)

    search = search.lower().strip()

    memories = []

    for node_id, data in nx_graph.nodes(data=True):

        label = str(data.get("label", node_id))
        current_type = str(data.get("entity_type", "unknown"))
        current_status = str(data.get("status", DEFAULT_MEMORY_STATUS))

        if search and search not in label.lower() and search not in str(node_id).lower():
            continue

        if entity_type != "All" and current_type != entity_type:
            continue

        if status != "All" and current_status != status:
            continue

        memories.append({
            "id": node_id,
            "label": label,
            "entity_type": current_type,
            "status": current_status,
            "degree": nx_graph.degree(node_id),
        })

    memories.sort(
        key=lambda item: (-item["degree"], item["label"].lower())
    )

    return memories