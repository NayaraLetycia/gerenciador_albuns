import os
import pandas as pd
import discogs_client
from fuzzywuzzy import fuzz

# Token da variável de ambiente
DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN")
if not DISCOGS_TOKEN:
    raise ValueError("Token do Discogs não encontrado! Configure DISCOGS_TOKEN.")

# Cliente Discogs
D = discogs_client.Client('DiscogsAlbumApp/1.0', user_token=DISCOGS_TOKEN)


def buscar_album(banda_nome, album_nome, ano_album=None, formato=None):
    # Busca no Discogs
    results = D.search(album_nome, artist=banda_nome, type='release', year=ano_album, format=formato)
    releases = list(results)

    if not releases:
        print("Nenhum álbum encontrado!")
        return None

    # Mostrar opções
    print("\nResultados encontrados:")
    for i, r in enumerate(releases, 1):
        print(f"[{i}] {r.title} - {r.year if hasattr(r, 'year') else 'Ano desconhecido'} - Formato: {r.formats}")

    escolha = int(input("\nDigite o número do álbum que deseja cadastrar: ")) - 1
    escolhido = releases[escolha]

    # Pegar detalhes do release
    release_data = D.release(escolhido.id)
    preco_min = release_data.marketplace_stats.get("lowest_price", "N/A")
    preco_max = release_data.marketplace_stats.get("highest_price", "N/A")

    registro = {
        "Banda": banda_nome,
        "Álbum": escolhido.title,
        "Ano": escolhido.year if hasattr(escolhido, "year") else ano_album,
        "Formato": ", ".join(escolhido.formats) if hasattr(escolhido, "formats") else formato,
        "Preço Mínimo": preco_min,
        "Preço Máximo": preco_max,
        "Imagem": escolhido.data.get("cover_image", "N/A")
    }

    print("\n📀 Confirme os dados a serem inseridos:")
    for k, v in registro.items():
        print(f"- {k}: {v}")

    confirmar = input("\nDeseja salvar este álbum no Excel? (s/n): ").lower()
    if confirmar == "s":
        salvar_planilha(registro)
        print("✅ Álbum salvo com sucesso!")
    else:
        print("❌ Operação cancelada.")


def salvar_planilha(registro, arquivo_planilha="colecao_albuns.xlsx"):
    df = pd.DataFrame([registro])
    if os.path.exists(arquivo_planilha):
        df.to_excel(arquivo_planilha, index=False, mode="a", header=False)
    else:
        df.to_excel(arquivo_planilha, index=False)


if __name__ == "__main__":
    banda = input("Digite o nome da banda: ")
    album = input("Digite o nome do álbum: ")
    ano = input("Digite o ano (opcional): ")
    formato = input("Digite o formato (ex: CD, LP, Cassette): ")

    buscar_album(banda, album, ano if ano else None, formato if formato else None)
