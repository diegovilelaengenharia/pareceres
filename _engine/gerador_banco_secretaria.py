import os
import sys

# Tenta carregar bibliotecas extratoras
try:
    from pypdf import PdfReader
    has_pdf = True
except ImportError:
    has_pdf = False

try:
    import win32com.client as win32
    has_win32 = True
except ImportError:
    has_win32 = False

if len(sys.argv) < 2:
    print("Uso: python gerador_banco_secretaria.py <CAMINHO_PASTA_DOS_DOCUMENTOS>")
    sys.exit(1)

pasta_alvo = sys.argv[1]
arquivo_saida = "conhecimento_secretaria_rag.txt"

if not os.path.isdir(pasta_alvo):
    print(f"Pasta '{pasta_alvo}' não encontrada.")
    sys.exit(1)

textos = []

print(f"Varrendo pasta '{pasta_alvo}' para abstrair Conhecimento Administrativo...\n")

word = None
if has_win32:
    try:
        word = win32.Dispatch('Word.Application')
        word.Visible = False
    except:
        word = None

count = 0
for arq in os.listdir(pasta_alvo):
    path = os.path.abspath(os.path.join(pasta_alvo, arq))
    texto = ""

    if arq.lower().endswith('.pdf') and has_pdf:
        try:
            texto = PdfReader(path).pages[0].extract_text()
        except Exception as e:
            pass

    elif arq.lower().endswith('.doc') and word:
        try:
            doc = word.Documents.Open(path)
            texto = doc.Content.Text
            doc.Close()
        except:
            pass

    if texto.strip():
        # Limpa o texto condensando formatação para inteligência GEM
        linhas = [l.strip() for l in texto.split('\n') if l.strip()]
        texto_limpo = "\n".join(linhas)
        textos.append(f"--- MODELO DE DOC: {arq} ---\n{texto_limpo}\n")
        count += 1
        print(f"[OK] Lido e estruturado: {arq}")

if word:
    word.Quit()

if textos:
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("\n\n############################\n".join(textos))
    print(f"\nSucesso! Os {count} modelos foram compilados no arquivo '{arquivo_saida}'.")
    print("Faça Upload deste TXT aos arquivos de Conhecimento do seu Assistente GEM.")
else:
    print("\nNenhum texto pôde ser lido. Verifique os Pdfs ou se o módulo pywin32 falhou.")
