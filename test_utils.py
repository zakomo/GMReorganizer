import utils


def test_sanitize_names_html_entity_with_hash():
    assert utils.sanitize_name("c&#39;erano") == "c'erano"


def test_sanitize_names_html_entity_with_name():
    assert utils.sanitize_name("hello&amp;g'day") == "hello&g'day"


def test_sanitize_names_with_pathsep_linux():
    assert utils.sanitize_name("hello/world") == "hello-world"


def test_sanitize_names_with_pathsep_win():
    assert utils.sanitize_name("hello\\world") == "hello-world"


def test_sanitize_names_with_spaces():
    assert utils.sanitize_name(" hello world \t") == "hello world"


def test_sanitize_names_mixed():
    assert utils.sanitize_name(" The night &amp; the day are &#39;rad") == "The night & the day are 'rad"
