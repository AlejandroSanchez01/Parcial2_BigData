import boto3
import urllib.request
import datetime


def download_page(url, bucket, nombre):

    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    today = datetime.date.today().strftime('%Y-%m-%d')
    s3 = boto3.resource('s3')
    s3.Object(bucket, 'headlines/raw/{}{}.html'.format(
        nombre, today)).put(Body=content)
    return content


download_page('https://www.eltiempo.com', 'bucket-news23', 'elTiempo-')
download_page('https://www.elespectador.com', 'bucket-news23', 'elEspectador-')
