import pickle # https://docs.python.org/3/library/pickle.html
import os # https://docs.python.org/3/library/os.html
import nltk # https://www.nltk.org
import sys # https://docs.python.org/pt-br/3/library/sys.html

"""
    O etiquetador é responsável pelo processo de definição da classe gramatical 
    das palavras, de acordo com as funções sintáticas.
"""
def criar_etiquetador():
    if os.path.isfile('mac_morpho.pkl'):
        # Carregando um modelo treinado
        input = open('mac_morpho.pkl', 'rb')
        tagger = pickle.load(input)
        input.close()
    else:
        # Obtendo as sentencas etiquetadas do corpus mac_morpho
        tagged_sents = nltk.corpus.mac_morpho.tagged_sents()
        
        # Instanciando etiquetador e treinando com as sentenças etiquetadas
        tagger = nltk.UnigramTagger(tagged_sents)
        # t2 = nltk.BigramTagger(tagged_sents, backoff=t1)    
        # tagger = nltk.TrigramTagger(tagged_sents, backoff=t2)

        # Salvar um modelo treinado em um arquivo para mais tarde usa-lo.
        output = open('mac_morpho.pkl', 'wb')
        pickle.dump(tagger, output, -1) 
        output.close()
    return tagger

"""
    Valida e retorna os argumentos passando pela linha de comando.
    return (base: String, consulta: String)
"""
def validar_argumentos():
    # É necessário passar como argumento o caminho para as bases e o caminho para
    # a consulta
    if len(sys.argv) <= 2:
        print('Número de argumentos inválido')
        exit()

    # receber  um argumento como  entrada  pela linha  de comando. Este argumento 
    # especifica o caminho de um arquivo texto que contém os caminhos de todos os
    # arquivos que compõem a base, cada um em uma linha.
    (base, consulta) = (sys.argv[1], sys.argv[2])

    # se caminho nao é arquivo ou nao existe o programa fecha
    if not os.path.isfile(base) or not os.path.isfile(consulta):
        print('Caminho para base inválido.')
        exit()
    
    return (base, consulta)
    