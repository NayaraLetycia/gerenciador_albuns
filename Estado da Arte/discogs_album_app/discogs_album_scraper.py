import pandas as pd
from datetime import datetime
import os
import discogs_client
from fuzzywuzzy import fuzz

# Insira seu token Discogs abaixo
DISCOGS_TOKEN = ''  # Exemplo: 'abc123...'
D = discogs_client.Client('DiscogsAlbumApp/1.0', user_token=DISCOGS_TOKEN)

def preencher_planilha(banda_nome, album_nome, ano_album, arquivo_planilha='albuns.xlsx'):
    results = D.search(album_nome, artist=banda_nome, type='release', year=ano_album)
    releases = list(results)
    if not releases:
        print('Nenhum álbum encontrado no Discogs!')
        return
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
        return
    df = pd.DataFrame(dados)
    if os.path.exists(arquivo_planilha):
        df_antigo = pd.read_excel(arquivo_planilha)
        df = pd.concat([df_antigo, df], ignore_index=True)
    df.to_excel(arquivo_planilha, index=False)
    print(f'{len(dados)} registro(s) inserido(s) na planilha {arquivo_planilha}!')
