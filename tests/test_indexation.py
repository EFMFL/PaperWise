import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.indexation as indexation


class FakeCollection:
    def __init__(self):
        self.upserts = []

    def upsert(self, **kwargs):
        self.upserts.append(kwargs)

    def count(self):
        return sum(len(item.get("ids", [])) for item in self.upserts)


class FakeModel:
    def encode(self, textes, show_progress_bar=False):
        return [[0.0] for _ in textes]


class IndexationTest(unittest.TestCase):
    def test_indexer_chunks_indexes_all_chunks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            chemin_chunks = Path(tmpdir) / "chunks.json"
            chunks = [
                {"id": f"chunk_{i}", "texte": f"texte de test {i}", "source": "doc.pdf", "page": 1}
                for i in range(25)
            ]
            chemin_chunks.write_text(json.dumps(chunks), encoding="utf-8")

            indexation.FICHIER_CHUNKS = str(chemin_chunks)
            indexation.collection = FakeCollection()
            indexation.modele = FakeModel()

            indexation.indexer_chunks()

            self.assertEqual(indexation.collection.count(), 25)


if __name__ == "__main__":
    unittest.main()
