import unittest
from get_urls_from_html import get_urls_from_html, get_images_from_html

class TestUrls(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_multiple(self):
            input_url = "https://crawler-test.com"
            input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><br /><a href="https://home.donaie.uk"><span>Harri Home</span></a></body></html>'
            actual = get_urls_from_html(input_body, input_url)
            expected = ["https://crawler-test.com", "https://home.donaie.uk"]
            self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
            input_url = "https://crawler-test.com"
            input_body = '<html><body><a href="/testicles.txt"><span>Boot.dev</span></a></body></html>'
            actual = get_urls_from_html(input_body, input_url)
            expected = ["https://crawler-test.com/testicles.txt"]
            self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_multiple(self):
                input_url = "https://crawler-test.com"
                input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><br /><a href="/thisismysecondtext.exe"><span>Harri Home</span></a></body></html>'
                actual = get_urls_from_html(input_body, input_url)
                expected = ["https://crawler-test.com", "https://crawler-test.com/thisismysecondtext.exe"]
                self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><br /><img src="https://crawler-test.com/logonumerodos.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/logonumerodos.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)