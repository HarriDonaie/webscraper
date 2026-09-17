import unittest
from get_first_paragraph_from_html import get_first_paragraph_from_html


class TestParagraph(unittest.TestCase):
    def test_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """
            <html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>
        """
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_no_para(self):
        input_body = """
            <html><body>
            <h1>Outside paragraph.</h1>
            <main>
                <div>Main paragraph.</div>
            </main>
        </body></html>
        """
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
