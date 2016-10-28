from flask import render_template_string


def test_jinja2_markdown_filter():
    source = """
        {% markdown %}
        ### Heading 3
        {% endmarkdown %}
        """
    html = render_template_string(source)
    assert u'<h3 id="heading-3">Heading 3</h3>' in html
