import re # https://docs.python.org/3/library/re.html
import utils # minha biblioteca de funções
import indice_invertido

# Valida e retorna os argumentos da linha de comando
(caminhoBase, caminhoConsulta) = utils.validar_argumentos()

# abre a base informada e le seus documentos
base = open(caminhoBase, 'r')
documentos = base.read().split('\n')
base.close()

# pega o diretorio da base
pastas = caminhoBase.split('/')
diretorio = ''.join(pastas[0:len(pastas)-1]) + '/' if len(pastas)-1 != 0 else ''

(indice, stemmer) = indice_invertido.gerar_indice(documentos, diretorio)

# função lambda para pegar os documentos em que determinado indice aparece
documentos_indice = lambda i: {d[0] for d in indice[i]} if i in indice.keys() else {}

# pega o conjunto da negação do termo
conjunto_not = lambda i: conjuntoDocumentos.difference(documentos_indice(i.replace('!','')))

# avalia se o termo é nulo ou não e retorna o conjunto dos indice correto 
avalia_termo = lambda i: documentos_indice(i) if nao_eh_negado(i) else conjunto_not(i)

# função lambda pra verificar se é um termo negado
nao_eh_negado = lambda t: '!' not in t

# funcao lambda para extrair radicais
ext_rad = lambda t: stemmer.stem(t)

# função lambda para extrair radical dos termos
extrair_radical = lambda t: ext_rad(t) if nao_eh_negado(t) else '!' + ext_rad(t[1:])

extrair_radicais = lambda ts: [extrair_radical(t) for t in ts]

# lambda para pegar os conjuntos dos termos no and
termos_and = lambda ts: [t for t in ts.split(' & ')]

# abre o arquivo de consulta, lê o conteúdo e fecha o arquivo
arq = open(caminhoConsulta, 'r')
consulta = arq.read().strip()
arq.close()

def intersecao_and(termos):
    conjuntoAnd = [avalia_termo(e) for e  in extrair_radicais(termos_and(termos))]
    res = conjuntoAnd[0]
    for c in conjuntoAnd[1:]:
        res = res.intersection(c)
    return res
    
# conjunto de todos os documentos presentes na base
conjuntoDocumentos = {*range(1, len(documentos)+1)}

# todos os termos da consulta
termosConsulta = re.findall(r"[!\w][\w]*", consulta)
termosConsulta = extrair_radicais(termosConsulta)

# divide a consulta em sub-consultas
subConsultas = consulta.split(' | ')

conjuntoTermos = [intersecao_and(e) if '&' in e else avalia_termo(extrair_radical(e)) for e in subConsultas]

res = conjuntoTermos[0]
for c in conjuntoTermos[1:]:
    res = res.union(c)
    
arquivo = open('resposta.txt', 'w')
arquivo.write(f'{len(res)}\n')
for r in res:
    arquivo.write(f'{documentos[r-1]}\n')
arquivo.close()
