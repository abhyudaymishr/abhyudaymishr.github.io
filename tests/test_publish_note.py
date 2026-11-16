import unittest
import sys
from pathlib import Path
import contextlib
import io
import tempfile
from unittest.mock import patch

# Add repo root to sys.path so scripts can be imported
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.publish_note import slugify, extract_title_and_body, HTMLToMarkdown, find_matching_post
from scripts import publish_note

class TestPublishNote(unittest.TestCase):
    def test_notes_update_preserves_authored_metadata_and_published_url(self):
        with tempfile.TemporaryDirectory() as directory:
            posts = Path(directory)
            post = posts / '2026-03-10-original-title.md'
            retained = '''seo_title: "Quantum Computing Research | Abhyuday Mishra"
description: >-
  A carefully written summary of the research.
  This continuation belongs to the description.
topics:
  - Quantum Computing
  - Scientific ML
math: true
project_ref: /projects/qudit-circuit-framework/
permalink: /blog/stable-address/
'''
            post.write_text('---\ntitle: "Original title"\ndate: 2026-03-10\nlast_modified_at: 2026-03-11\nnote_id: "note-123"\n'+retained+'---\nOld body.\n')
            with patch.object(publish_note, 'POSTS_DIR', posts), contextlib.redirect_stdout(io.StringIO()):
                filename = publish_note.publish_post_content('# Updated title\n\nNew body.\n#Update', note_id='note-123', push=False)
            updated = post.read_text()
            self.assertEqual(filename, post.name)
            self.assertIn(retained, updated)
            self.assertIn('title: "Updated title"', updated)
            self.assertIn('date: 2026-03-10', updated)
            self.assertEqual(updated.count('last_modified_at:'), 1)
            self.assertNotIn('last_modified_at: 2026-03-11', updated)
            self.assertIn('New body.', updated)
            self.assertNotIn('Old body.', updated)
            self.assertEqual(len(list(posts.glob('*.md'))), 1)

    def test_slugify(self):
        self.assertEqual(slugify("Why Qudits Matter!"), "why-qudits-matter")
        self.assertEqual(slugify("  Neural   Operators & Geometry  "), "neural-operators-geometry")
        self.assertEqual(slugify("Café & Résumé"), "café-résumé")

    def test_extract_title_and_body(self):
        raw = "# My Research Post\n\n#Publish\n\nThis is the content about neural operators."
        title, body = extract_title_and_body(raw)
        self.assertEqual(title, "My Research Post")
        self.assertIn("This is the content about neural operators.", body)
        self.assertNotIn("#Publish", body)

    def test_extract_title_ignores_publish_tags(self):
        raw = "#Publish\n# Actual Title\n\nBody paragraph."
        title, body = extract_title_and_body(raw)
        self.assertEqual(title, "Actual Title")
        self.assertEqual(body.strip(), "Body paragraph.")

    def test_html_to_markdown(self):
        parser = HTMLToMarkdown()
        parser.feed("<div><h1>Header</h1><p>Text with <b>bold</b> and <a href=\"https://example.com\">link</a>.</p></div>")
        md = parser.get_markdown()
        self.assertIn("# Header", md)
        self.assertIn("**bold**", md)
        self.assertIn("[link](https://example.com)", md)

    def test_find_matching_post(self):
        existing = [
            {'title': 'Why Qudits Matter', 'date': '2026-03-10', 'note_id': 'x-coredata://123', 'slug': 'why-qudits-matter', 'file_path': Path('2026-03-10-why-qudits-matter.md'), 'filename': '2026-03-10-why-qudits-matter.md'}
        ]
        # Match by note_id
        match = find_matching_post('x-coredata://123', 'Different Title', existing)
        self.assertIsNotNone(match)
        self.assertEqual(match['slug'], 'why-qudits-matter')

        # Match by title
        match2 = find_matching_post(None, 'Why Qudits Matter', existing)
        self.assertIsNotNone(match2)
        self.assertEqual(match2['date'], '2026-03-10')

        # No match
        self.assertIsNone(find_matching_post('unknown-id', 'Brand New Post', existing))

if __name__ == '__main__':
    unittest.main()
