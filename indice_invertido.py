import nltk # https://www.nltk.org
import utils # minha biblioteca de funções

# Assuma que nesses  arquivos  texto, palavras  são separadas por um  ou mais
# dos seguintes caracteres: espaço em branco ( ), ponto (.), reticências(...)
# vírgula (,), exclamação (!), interrogação (?) ou enter (\n).
pontuacao = [',', '!', '?', '\n']

# PREP = preposição, ART = artigo, KC = conjunção coordenativa, KS = conjução
# subordinativo
retirarClassificacao = ['PREP', 'ART', 'KC', 'KS']

# entendimento do significado de um documento.
stopwords = nltk.corpus.stopwords.words('portuguese')

etiquetador = utils.criar_etiquetador()

# A processing interface for removing morphological  affixes from words. This 
# process is known as stemming.
# https://www.nltk.org/api/nltk.stem.html
stemmer = nltk.stem.RSLPStemmer()

def gerar_indice(documentos, diretorio):
    indicesInvertidos = {}
    for numeroArquivo, documento in enumerate(documentos):
        # abre e le o conteudo de todos os documentos
        file = open(diretorio + documento)
        doc = file.read()
        file.close()

        # caracteres '.', ',', '!', '?', '...' e '\n' não devem ser considerados.
        # se o caracter for . troca por um espaço
        semPontuacao = [p if p != '.' else ' ' for p in doc if p not in pontuacao]
        palavras = ''.join(semPontuacao).split(' ')

        # stopwords não devem ser levadas em conta na geração do índice invertido
        semStopwords = [p for p in palavras if p not in stopwords]
        semEspacos = [p for p in semStopwords if p not in ' ']

        # classificação gramatical
        etiquetados = etiquetador.tag(semEspacos)

        # sem as classificações de preposição, conjunção e artigo
        semClassificacoes = [p[0] for p in etiquetados if p[1] not in retirarClassificacao]
        
        # extrair os radicais das palavras para o índice invertido
        radicais = [stemmer.stem(p) for p in semClassificacoes]
        
        # faz um indice invertido para o documento n
        indice = {p:(numeroArquivo + 1, radicais.count(p)) for p in radicais}

        # junta todos os indices em um só  indice invertido. Queria  muito fazer
        # com compreesão, mas fui incapaz :C
        for chave, valor in indice.items():
            if chave not in indicesInvertidos.keys():
                indicesInvertidos[chave] = []
            indicesInvertidos[chave].append(valor)

    # ordena o indice invertido pela chave
    indice = dict(sorted(indicesInvertidos.items()))

    # escrev em arquivo o indice invertido
    # escreve o indice invertido no arquivo indice.txt
    arquivo = open('indice.txt', 'w')
    for chave, valor in indice.items():
        arquivo.write(f'{chave}:')
        for v in valor:
            arquivo.write(f' {v[0]},{v[1]}')
        arquivo.write('\n')
    arquivo.close()

    return (indice, stemmer)
    