from noticias import download_page
from unittest import mock


def test_download_page(mocker):

    content = "<html><head><title>Example</title></head> \
    <body><h1>Example</h1></body></html>"
    mocker.patch('urllib.request.urlopen', return_value=mock.Mock(
        read=lambda: content.encode()))
    respuesta = download_page(
        'https://www.eltiempo.com', 'bucket-news23', 'elTiempo-')
    assert respuesta == content
