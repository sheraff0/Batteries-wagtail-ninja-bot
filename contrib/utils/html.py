from bs4 import BeautifulSoup


def unpack_elements(html, join=None):
    soup = BeautifulSoup(html or "", "html.parser")
    _elements = soup.find_all("p")
    _elements_text = [_text for el in _elements if (_text := el.text)] \
        or [soup.text]
    return join.join(_elements_text) if join else _elements_text
