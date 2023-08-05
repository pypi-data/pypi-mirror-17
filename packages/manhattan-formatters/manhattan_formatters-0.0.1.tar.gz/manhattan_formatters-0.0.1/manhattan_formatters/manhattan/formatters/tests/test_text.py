from manhattan.formatters import text


def test_slugify():
    """Return the given string formatted as a slug"""
    assert text.slugify('"This is my blog title!"') == 'this-is-my-blog-title'

def test_text_to_html():
    """
    Return a HTML version of the specified text.
    """
    s = """
<foo>
bar

This is a link http://www.example.com
    """.strip()

    # Check output for `inline=True` and `convert_urls=True`
    assert text.text_to_html(s, True, True) == ('&lt;foo&gt;<br>bar<br>'
            '<br>This is a link <a href="http://www.example.com">'
            'http://www.example.com</a>')

    # Check output for `inline=False` and `convert_urls=True`
    assert text.text_to_html(s, False, True) == ('<p>&lt;foo&gt;<br>bar</p>'
            '<p>This is a link <a href="http://www.example.com">'
            'http://www.example.com</a></p>')

    # Check output for `inline=True` and `convert_urls=False`
    assert text.text_to_html(s, True, False) == \
            '&lt;foo&gt;<br>bar<br><br>This is a link http://www.example.com'

    # Check output for `inline=False` and `convert_urls=False`
    assert text.text_to_html(s, False, False) == ('<p>&lt;foo&gt;'
            '<br>bar</p><p>This is a link http://www.example.com</p>')

def test_yes_no():
    """Return `'Yes'` if a value coerces to `True`, `'No'` if not."""
    assert text.yes_no(True) == 'Yes'
    assert text.yes_no(False) == 'No'
    assert text.yes_no('foo') == 'Yes'
    assert text.yes_no(None) == 'No'