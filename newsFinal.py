import boto3
from bs4 import BeautifulSoup
import unicodedata
from datetime import date

S3_BUCKET = 'bucket-news23'
fecha = date.today()

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')


def extraerTiempo(file):
    contenido = s3.get_object(Bucket=S3_BUCKET, Key=file)["Body"].read()
    soup = BeautifulSoup(contenido, 'html.parser')

    texto = 'titulo,categoria,link\n'
    enlaces_vistos = []
    for articles in soup.find_all('article'):
        for links in articles.find_all('a', class_='title page-link'):
            try:
                link = links["href"]
                if link not in enlaces_vistos:
                    enlaces_vistos.append(link)
                    categoria = link.split('/')[1]
                    titulo = links.text.strip()
                    texto += f'"{titulo}","{categoria}","{link}"\n'
            except KeyError:
                pass

    url = "headlines/final/periodico=elTiempo/year=" + \
        str(fecha.year)+"/month="+str(fecha.strftime('%m'))+"/elTiempo"
    s3_resource.Object(S3_BUCKET, url+'{}.csv'.format(
      fecha.strftime('%Y-%m-%d'))).put(Body=texto)


def extraerEspectador(file):
    contenido = s3.get_object(Bucket=S3_BUCKET, Key=file)["Body"].read()
    soup = BeautifulSoup(contenido, 'html.parser')
    titulos = []
    categorias = []
    links = []

    for articles in soup.find_all('div', class_='Card-Container'):
        a = articles.find_all('h4', class_='Card-Section Section')
        text = articles.find_all('a')

        a = [t.text for t in text]
        cont = 0
        for i in a:
            if (i != ""):
                cont = cont + 1
                if (cont == 1):
                    categorias.append(i)
                if (cont == 2):
                    titulos.append(i.replace(",", ""))
            if (cont == 3):
                break

        titulo_link = articles.find_all(
            'h2', class_='Card-Title Title Title')
        try:
            titulo_link = articles.find_all(
                'h2', class_='Card-Title Title Title_main')
            soup = BeautifulSoup(str(titulo_link), 'html.parser')

            # Seleccionar el elemento <a> dentro del <h2>
            enlace = soup.find('h2').find('a')

            # Obtener el valor del atributo href
            url = enlace.get('href')
            # print(url)
            links.append(url)
        except AttributeError:
            try:
                titulo_link = articles.find_all(
                    'h2', class_='Card-Title Title Title')
                soup = BeautifulSoup(str(titulo_link), 'html.parser')

                # Seleccionar el elemento <a> dentro del <h2>
                enlace = soup.find('h2').find('a')

                # Obtener el valor del atributo href
                url = enlace.get('href')
                links.append(url)
                # print(url)
            except KeyError:
                pass

    texto = ""
    texto = "categoria,titulo,link" + "\n"

    for i in range(0, 10):
        texto += '"' + categorias[i] + '",' + '"' + titulos[i] + \
            '",' + '"' + links[i] + '"' + "\n"

    # Utilizar la función normalize para eliminar las tildes

    texto = unicodedata.normalize('NFKD', texto).encode(
      'ASCII', 'ignore').decode('utf-8')
    url = "headlines/final/periodico=elEspectador/year=" + str(
      fecha.year) + "/month=" + str(fecha.strftime('%m')) + "/elEspectador"
    s3_resource.Object(S3_BUCKET, url + '{}.csv'.format(
      fecha.strftime('%Y-%m-%d'))).put(Body=texto)
    return texto


extraerTiempo("headlines/raw/elTiempo-" + str(fecha.year) + "-" + str(
  fecha.strftime('%m')) + "-" + str(fecha.strftime('%d')) + ".html")
extraerEspectador("headlines/raw/elEspectador-" + str(fecha.year) + "-" + str(
  fecha.strftime('%m')) + "-" + str(fecha.strftime('%d')) + ".html")
