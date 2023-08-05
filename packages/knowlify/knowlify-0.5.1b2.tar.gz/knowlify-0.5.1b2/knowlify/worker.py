import os
import sys
import config
from codecs import open
from lxml import html


def output_page(page, path=None):
    """
    :type page: html.HtmlElement
    :returns path: os.path.genericpath
    """

    if path is None:
        # path = os.path.join(config.DATA_DIR, 'knowl_'+ page.text_content().lstrip('\r\n')[:11] + str(time.time()) + '.html')
        path = os.path.join(config.DATA_DIR, 'knowl_' + page.text_content().lstrip('\r\n')[:11] + '.html')

    # if os.path.isfile(path):
    #     path += str(time.time())

    try:
        with open(path, 'w') as f:
            f.write(html.tostring(page))
    except OSError:
        sys.stderr('Unable to write output for filename: %s' % path)
        return 2

    return path


def output_dummy(page, len=5):
    assert isinstance(page, html.HtmlElement)
    text = [e.text_content().strip('\r\n') for e in page.iter('p')]
    text = text[:len]
    name = 'knowl_' + text[0].split(' ')[0] + '.html'
    path = os.path.join(config.DATA_DIR, name)

    # if os.path.isfile(name):
    #     name += str(time.time())

    try:
        with open(path, 'w', encoding='utf-8') as f:
            [f.write('<p>' + t + '</p>') for t in text]

    except OSError:
        sys.stderr('Unable to write output for dummy file: %s' % name)
        return 2

    return name


if __name__ == "__main__":
    pass
