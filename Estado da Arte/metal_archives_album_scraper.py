import pandas as pd
from datetime import datetime
import os

# NOVO: Usar Discogs
import discogs_client
from fuzzywuzzy import process, fuzz

D = discogs_client.Client('MetalAlbumApp/1.0')

# Função para buscar banda no Metal Archives

def buscar_banda(banda_nome):
    url = f'https://www.metal-archives.com/search?searchString={banda_nome.replace(" ", "+")}&type=band_name'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    resultados = soup.select('table#searchResults tr td a')
    bandas = [(a.text.strip(), a['href']) for a in resultados if a['href'].startswith('https://www.metal-archives.com/bands/')]
    if not bandas:
        return None, None
    nomes = [b[0] for b in bandas]
    melhor, score = process.extractOne(banda_nome, nomes)
    for nome, link in bandas:
        if nome == melhor:
            return nome, link
    return bandas[0]

# Função para buscar álbuns da banda

def buscar_albuns(banda_url):
    resp = requests.get(banda_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    albuns = []
    for row in soup.select('table#discography tr'):  # pode precisar ajustar
        cols = row.find_all('td')
        if len(cols) >= 4:
            album_nome = cols[0].text.strip()
            album_url = cols[0].find('a')['href'] if cols[0].find('a') else None
            ano = cols[1].text.strip()
            tipo = cols[2].text.strip()
            albuns.append({'nome': album_nome, 'url': album_url, 'ano': ano, 'tipo': tipo})
    return albuns

# Função para buscar detalhes do álbum

def buscar_detalhes_album(album_url):
    resp = requests.get(album_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    detalhes = {}
    detalhes['url'] = album_url
    detalhes['tracklist'] = '\n'.join([li.text.strip() for li in soup.select('ol.trackList li')])
    infos = soup.select('div#album_info dl')
    for dl in infos:
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')
        for dt, dd in zip(dts, dds):
            detalhes[dt.text.strip(': ')] = dd.text.strip()
    return detalhes

# Função principal



def preencher_planilha(banda_nome, album_nome, ano_album, arquivo_planilha='albuns.xlsx'):
    # Busca no Discogs
    results = D.search(album_nome, artist=banda_nome, type='release', year=ano_album)
    releases = list(results)
    if not releases:
        print('Nenhum álbum encontrado no Discogs!')
        return
    # Fuzzy match para o nome do álbum
    melhores = [r for r in releases if fuzz.token_set_ratio(r.title.lower(), album_nome.lower()) >= 80]
    if not melhores:
        melhores = releases
    dados = []
    for r in melhores:
            r_data = r.data
            registro = {
                'Banda': banda_nome,
                'Álbum': r.title,
                'Ano': r.year if hasattr(r, 'year') else ano_album,
                'Tipo': r_data.get('format', [''])[0] if 'format' in r_data else '',
                'Data de inserção': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Gênero': ', '.join(r_data.get('genre', [])),
                'Estilos': ', '.join(r_data.get('style', [])),
                'País': r_data.get('country', ''),
                'Label': ', '.join(r_data.get('label', [])) if 'label' in r_data else '',
                'Tracklist': '\n'.join([t.title for t in getattr(r, 'tracklist', [])])
            }
            dados.append(registro)
    if not dados:
        print('Nenhum dado válido encontrado!')
    df = pd.DataFrame(dados)

        # --- Todas as funções antigas de scraping removidas ---
    df = pd.DataFrame(dados)
