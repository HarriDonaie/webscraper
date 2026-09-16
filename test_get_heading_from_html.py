import unittest
from get_heading_from_html import get_heading_from_html

class TestHeading(unittest.TestCase):
    def testNoH1(self):
        input_html = """
        <html>
            <body>
                <h2>Welcome to Boot.dev</h2>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def testNoH1orH2(self):
            input_html = """
        <html>
            <body>
                <p>Welcome to Boot.dev</p>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
        </html>
        """
            actual = get_heading_from_html(input_html)
            expected = "Welcome to Boot.dev"
            self.assertEqual(actual, expected)

    def testNoH2(self):
            input_html = """
        <html>
            <body>
                <h1>Welcome to Boot.dev</h1>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
        </html>
        """
            actual = get_heading_from_html(input_html)
            expected = "Welcome to Boot.dev"
            self.assertEqual(actual, expected)

    def testNormal(self):
            input_html = """
        <html>
            <body>
                <h1>Welcome to Boot.dev</h1>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
        </html>
        """
            actual = get_heading_from_html(input_html)
            expected = "Welcome to Boot.dev"
            self.assertEqual(actual, expected)



if __name__ == "__main__":
    unittest.main()