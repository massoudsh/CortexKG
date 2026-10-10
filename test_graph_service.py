import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

from graph_service import initialize_graph, sample_knowledge_graph, update_graph


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


if __name__ == "__main__":
    unittest.main()
