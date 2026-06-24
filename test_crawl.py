import unittest

from crawl import ( 
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,
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


class TestGetUrlsFromHTML(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
 
    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)
 
    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a href="/path/one">First</a>
            <a href="https://other-site.com/page">Second</a>
        </body></html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/path/one",
            "https://other-site.com/page",
        ]
        self.assertEqual(actual, expected)
 
    def test_get_urls_from_html_no_href(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a>No link here</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
 
    def test_get_urls_from_html_no_anchors(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><p>No links at all.</p></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
 
 
class TestGetImagesFromHTML(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
 
    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://cdn.crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://cdn.crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
 
    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <img src="/logo.png" alt="Logo">
            <img src="/banner.jpg" alt="Banner">
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://crawler-test.com/banner.jpg",
        ]
        self.assertEqual(actual, expected)
 
    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo with no src"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
 
    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><p>No images here.</p></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
class TestExtractPageData(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)
 
    def test_extract_page_data_h2_fallback(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Secondary Title</h2>
            <p>Some text.</p>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Secondary Title",
            "first_paragraph": "Some text.",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
 
    def test_extract_page_data_main_priority(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Title</h1>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
                <a href="/main-link">Main Link</a>
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Title",
            "first_paragraph": "Main paragraph.",
            "outgoing_links": ["https://crawler-test.com/main-link"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
 
    def test_extract_page_data_multiple_links_and_images(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Gallery</h1>
            <p>A gallery page.</p>
            <a href="/one">One</a>
            <a href="https://other.com/two">Two</a>
            <img src="/img1.png">
            <img src="https://cdn.other.com/img2.png">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Gallery",
            "first_paragraph": "A gallery page.",
            "outgoing_links": [
                "https://crawler-test.com/one",
                "https://other.com/two",
            ],
            "image_urls": [
                "https://crawler-test.com/img1.png",
                "https://cdn.other.com/img2.png",
            ],
        }
        self.assertEqual(actual, expected)
 
    def test_extract_page_data_empty_page(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()