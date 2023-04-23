from newsFinal import extraerEspectador
from datetime import date
import unicodedata

fecha = date.today()


def test_extraerEspectador(mocker):

    file = "headlines/raw/elEspectador-" + str(fecha.year) + "-" + str(
        fecha.strftime('%m')) + "-" + str(fecha.strftime('%d')) + ".html"
    texto_mock = 'ÁáÉéÍíÓóÚú'
    mocker.patch.object(unicodedata, 'normalize', return_value=texto_mock)
    respuesta = extraerEspectador(file)
    assert respuesta == ''
