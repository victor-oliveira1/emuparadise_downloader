#!/bin/python3
from urllib.request import Request, urlopen
from urllib.parse import unquote
from sys import argv
from re import findall
from html import unescape

url = argv[1]

if not 'https://www.emuparadise.me' in url:
    print('URL inválida.\nExemplos:\nhttps://www.emuparadise.me/PSX_on_PSP_ISOs/A-Train_(USA)/163325\nhttps://www.emuparadise.me/PSX_on_PSP_ISOs/A-Train_(USA)/163325-download')
    exit(1)
if not '-download' in url:
    url += '-download'

req = Request(url)
req.add_header('cookie', 'downloadcaptcha=1')
html = urlopen(req).read().decode()
try:
    link_download = unescape(findall('"/roms/get-download.php\S+"', html)[0].strip('"'))
except IndexError:
    print('Link inválido ou arquivo apagado.')
    exit(1)

req = Request('https://www.emuparadise.me' + link_download)
req.add_header('referer', url)
req = urlopen(req)
nome_arquivo = unquote(req.url.split('/')[-1])
tamanho_arquivo = int(req.getheader('Content-Length'))

print('Baixando:', nome_arquivo)
print('Tamanho:', str(int(tamanho_arquivo / 1000 / 1000)) + 'M')
status_download = 0
with open(nome_arquivo, 'wb') as arq:
    data = 2 * 1024 * 1024 #Mantém 2MB de cache
    while True:
        print(str(int(data * status_download * 100 / tamanho_arquivo)) + '%', end='\r')
        status_download += 1
        if not arq.write(req.read(data)):
            print('Download concluído')
            break
