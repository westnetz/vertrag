from vertrag.helpers import get_template

from jinja2 import Template

def test_get_template():
    t = get_template("vertrag/tests/fixtures/test_template.j2")
    assert t.render(test='A desired text.') == "This is a test template. A desired text."
