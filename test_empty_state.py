import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

from empty_state import empty_graph_content


class EmptyGraphStateTests(unittest.TestCase):
    def test_empty_graph_state_explains_how_to_start(self):
        heading, description, chat_anchor = empty_graph_content()

        self.assertEqual(heading, "No knowledge graph yet")
        self.assertIn("Start a conversation", description)
        self.assertEqual(chat_anchor, "#chat-interface")


if __name__ == "__main__":
    unittest.main()
