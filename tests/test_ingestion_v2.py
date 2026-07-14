import hashlib
import unittest

from local_scriptorium.ingestion import SourceDescriptor, build_chunks, build_passages, remove_gutenberg_wrapper


class IngestionV2Tests(unittest.TestCase):
    def test_wrapper_is_removed_deterministically(self):
        text = "head\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\nBody\n*** END OF THE PROJECT GUTENBERG EBOOK X ***\nfooter"
        self.assertEqual(remove_gutenberg_wrapper(text), "Body")

    def test_passage_ids_and_checksums_are_stable(self):
        descriptor = SourceDescriptor("TEST", "Author", "Work", "Translator", 1900)
        passages = build_passages("One\n\nTwo", descriptor)
        self.assertEqual(passages[0]["passage_id"], "TEST:p0001:l1-1")
        self.assertEqual(passages[1]["predecessor_id"], passages[0]["passage_id"])
        self.assertEqual(passages[0]["successor_id"], passages[1]["passage_id"])
        self.assertEqual(passages[0]["text_sha256"], hashlib.sha256(b"One").hexdigest())

    def test_chunks_do_not_cross_source_boundaries(self):
        first = build_passages("A\n\nB", SourceDescriptor("A", "a", "w", "t", 1900))
        second = build_passages("C", SourceDescriptor("B", "b", "w", "t", 1900))
        chunks = build_chunks(first + second, target_words=100, max_words=100)
        self.assertEqual([chunk["source_id"] for chunk in chunks], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
