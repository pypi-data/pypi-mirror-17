from jinja2.utils import escape as html_escape, urlize
from slugify import slugify as awesome_slugify

__all__ = [
    'slugify',
    'text_to_html',
    'yes_no'
    ]


def slugify(s):
    """
    Return the given string formatted as a slug
    (https://en.wikipedia.org/wiki/Semantic_URL#slug).
    """
    return awesome_slugify(s, to_lower=True)

def text_to_html(text, inline=False, convert_urls=True):
    """
    Return a HTML version of the specified text.

    If `inline` is True then new-lines will be converted line-breaks (`<br>`s),
    if `inline` is False then single new-lines will be converted to line-breaks
    (`<br>`s) and double new-lines will be converted to paragraphs.

    If `convert_urls` is True then URLs within the text are converted to links,
    if `convert_urls` is False then URLs are not converted.
    """
    if inline:
        # Convert URLs to links
        if convert_urls:
            inline_html = urlize(text)
        else:
            inline_html = str(html_escape(text))

        # Convert newlines to line-breaks / `<br>` tags
        inline_html = inline_html.replace('\n', '<br>')

        return inline_html

    else:
        # Convert the text to a list of paragraphs / <p> tags
        paragraphs = [text_to_html(p.strip(), True, convert_urls) \
            for p in text.split('\n\n') if p.strip()]

        print(paragraphs)

        # Join the paragraphs into a body and return it
        return '<p>' + '</p><p>'.join(paragraphs) + '</p>'

def yes_no(value):
    """Return `'Yes'` if a value coerces to `True`, `'No'` if not."""
    return 'Yes' if value else 'No'