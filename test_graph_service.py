import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

from graph_service import (
    format_graph_statistics,
    graph_statistics,
    initialize_graph,
    sample_knowledge_graph,
    update_graph,
)


class SampleKnowledgeGraphTests(unittest.TestCase):
    def test_sample_graph_contains_expected_connected_entities(self):
        graph = update_graph(initialize_graph(), sample_knowledge_graph())

        self.assertEqual(graph.number_of_nodes(), 7)
        self.assertEqual(graph.number_of_edges(), 6)
        self.assertTrue(graph.has_edge("maya", "api-migration"))
        self.assertEqual(graph.edges["maya", "api-migration"]["label"], "owns")
        self.assertTrue(graph.has_edge("token-retention-risk", "november-launch"))

    def test_sample_graph_can_be_loaded_more_than_once(self):
        graph = initialize_graph()
        sample = sample_knowledge_graph()

        update_graph(graph, sample)
        update_graph(graph, sample)

        self.assertEqual(graph.number_of_nodes(), 7)
        self.assertEqual(graph.number_of_edges(), 6)

    def test_graph_statistics_defaults_memories_to_unreviewed(self):
        graph = initialize_graph()
        graph.add_node("maya", status="confirmed")
        graph.add_node("omar")
        graph.add_edge("maya", "omar")

        self.assertEqual(
            graph_statistics(graph),
            {
                "nodes": 2,
                "edges": 1,
                "confirmed_memories": 1,
                "unreviewed_memories": 1,
            },
        )
        self.assertEqual(
            format_graph_statistics(graph),
            "CortexKG Statistics\n\nNodes: 2\nEdges: 1\nConfirmed Memories: 1\nUnreviewed Memories: 1",
        )


if __name__ == "__main__":
    unittest.main()
