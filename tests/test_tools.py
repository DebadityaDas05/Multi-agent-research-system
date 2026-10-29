from unittest.mock import MagicMock, patch
import requests
from tools import scrape_url, web_search

def test_scrape_url_html_cleaning():
    """Verify that scrape_url strips scripts, styles, nav, and footers."""
    mock_html = """
    <html>
        <head>
            <style>body { background: black; }</style>
            <script>console.log("tracking code");</script>
        </head>
        <body>
            <nav><a href="/">Home Menu</a></nav>
            <main>
                <h1>Quantum Computing Breakthrough</h1>
                <p>Researchers have achieved a new milestone in qubit coherence.</p>
            </main>
            <footer>Copyright 2026 Example Corp</footer>
        </body>
    </html>
    """
    mock_resp = MagicMock()
    mock_resp.text = mock_html
    mock_resp.status_code = 200

    with patch("requests.get", return_value=mock_resp):
        cleaned_text = scrape_url.invoke({"url": "https://example.com/article"})

    assert "Quantum Computing Breakthrough" in cleaned_text
    assert "qubit coherence" in cleaned_text
    assert "tracking code" not in cleaned_text
    assert "Home Menu" not in cleaned_text
    assert "Copyright 2026" not in cleaned_text

def test_scrape_url_length_truncation():
    """Verify that scrape_url limits payload size to 3000 characters."""
    long_text = "Data point " * 500  # > 5000 characters
    mock_html = f"<html><body><p>{long_text}</p></body></html>"
    mock_resp = MagicMock()
    mock_resp.text = mock_html

    with patch("requests.get", return_value=mock_resp):
        result = scrape_url.invoke({"url": "https://example.com/long"})

    assert len(result) <= 3000

def test_scrape_url_error_handling():
    """Verify that scrape_url gracefully catches network exceptions."""
    with patch("requests.get", side_effect=requests.RequestException("Connection timed out")):
        result = scrape_url.invoke({"url": "https://unreachable-domain.xyz"})

    assert "Could not scrape URL:" in result
    assert "Connection timed out" in result

def test_web_search_formatting():
    """Verify web_search formats results as expected."""
    mock_search_results = {
        "results": [
            {
                "title": "AI in Healthcare",
                "url": "https://example.com/ai-health",
                "content": "AI is accelerating diagnostic workflows significantly." * 10
            },
            {
                "title": "Robotics in Surgery",
                "url": "https://example.com/robotics",
                "content": "Surgical robots assist with precision procedures." * 10
            }
        ]
    }

    with patch("tools.tavily.search", return_value=mock_search_results):
        formatted = web_search.invoke({"query": "AI medicine"})

    assert "Title: AI in Healthcare" in formatted
    assert "URL: https://example.com/ai-health" in formatted
    assert "Title: Robotics in Surgery" in formatted
    assert "----" in formatted

