import unittest

from crawl import ( 
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
)

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_capitals(self):
        input_url = "https://www.BOOT.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.BOOT.dev/blog/path"
        self.assertEqual(actual, expected)

class TestGetHeadingFromHTML(unittest.TestCase):
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)
 
    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Secondary Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Secondary Title"
        self.assertEqual(actual, expected)
 
    def test_get_heading_from_html_h1_priority(self):
        input_body = """<html><body>
            <h1>Main Title</h1>
            <h2>Secondary Title</h2>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Main Title"
        self.assertEqual(actual, expected)
 
    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>No heading here.</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
 
    def test_get_heading_from_html_strips_whitespace(self):
        input_body = "<html><body><h1>   Test Title   </h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)
 
 
class TestGetFirstParagraphFromHTML(unittest.TestCase):
    def test_get_first_paragraph_from_html_basic(self):
        input_body = "<html><body><p>This is the first paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)
 
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
 
    def test_get_first_paragraph_from_html_no_main_fallback(self):
        input_body = """<html><body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)
 
    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>Just a heading</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
 
    def test_get_first_paragraph_from_html_multiple_in_main(self):
        input_body = """<html><body>
            <main>
                <p>First main paragraph.</p>
                <p>Second main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First main paragraph."
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()