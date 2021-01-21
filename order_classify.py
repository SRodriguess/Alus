# Comando:
# $ python3 order_classify.py caminho_arquivo > saida.tab

import sys

arquivo = sys.argv[1]

# 1º Passo
# Converte dado bruto em DICT +++++++++++++++++++++++++++++++++++++++++++ 
colum_control = 0 # Gerencia a coluna
count_line = 0
dic = {}
vec_subfamilia = {}
classe = ""
familia = ""
subfamilia = ""
vec_no_use_class = ["Low_complexity", "Satellite", "scRNA", "snRNA", "srpRNA", "rRNA", "tRNA", "Simple_repeat"] # Lista de classes que serão removidas
list_quants = {} # Armazena 'quantidade' de classes e familias

with open(arquivo, 'r') as file:
    # Para cada linha do arquivo
    for linha in file:
        count_line += 1
        linha = linha.replace("\n", "")
        # Ignorando primeira linha (cabecalho)
        if(count_line != 1):

            linha = linha.split("\t")

            if(colum_control == 0): # Caso esteja lendo coluna de classes
                classe = linha[colum_control]
                # inicializa classe
                dic[classe] = {}
                colum_control = 1
                
                # Registrando 'quantidade' de classe
                list_quants[classe] = {}
                list_quants[classe][classe+'_quant'] = {}
                list_quants[classe][classe+'_quant'] = linha[3]

            elif(colum_control == 1): # Caso esteja lendo coluna de familias
                familia = linha[colum_control]
                # inicializa familia
                dic[classe][familia] = {}
                colum_control = 2
                vec_subfamilia = {}

                # Registrando 'quantidade' de familia
                list_quants[classe][classe+"_"+familia] = {}
                list_quants[classe][classe+"_"+familia] = linha[3]

            elif(colum_control == 2): # Caso esteja lendo coluna de subfamilias

                if(linha[colum_control] == ""): # se chegou ao fim da subfamilia, inserir no dic. E verificar nova posicao de coluna.
                    # insere sub-familia
                    dic[classe][familia] = vec_subfamilia
                    while(linha[colum_control] == ""): # Verificando se proxima leitura será em classe ou familia e setando em 'colum_control'
                        colum_control -= 1
                        if(colum_control < 0):
                            break

                    if(colum_control == 1):
                        familia = linha[colum_control]
                        colum_control = 2
                        vec_subfamilia = {}

                        # Registrando 'quantidade' de familia
                        list_quants[classe][classe+"_"+familia] = {}
                        list_quants[classe][classe+"_"+familia] = linha[3]
                    
                    elif(colum_control == 0):
                        classe = linha[colum_control]
                        dic[classe] = {}
                        colum_control = 1                        

                        # Registrando 'quantidade' de classe
                        list_quants[classe] = {}
                        list_quants[classe][classe+'_quant'] = {}
                        list_quants[classe][classe+'_quant'] = linha[3]

                else: # enquanto estiver lendo subfamilia
                    subfamilia = linha[colum_control]
                    quant = linha[colum_control+1]
                    vec_subfamilia[subfamilia] = quant

    # insere ultima sub-familia
    dic[classe][familia] = vec_subfamilia


# 2º Passo
# Removendo classes não-utilizadas +++++++++++++++++++++++++++++++++++++++++++
for classe in vec_no_use_class:
    del dic[classe]


# 3º Passo
# Cria novo dict já ordenado e sem classes não-utilizadas ++++++++++++++++++++
list_classes_ord = sorted(list(dic))
new_dic = {}
for classe in list_classes_ord:
    new_dic[classe] = {}
    list_familia_ord = sorted(list(dic[classe]))
    for familia in list_familia_ord:
        new_dic[classe][familia] = {}
        lista_subfamilia_aux = {}
        lista_subfamilia_aux = dic[classe][familia] # copiando subfamilias para variavel auxiliar
        lista_subfamilia_aux = {k: v for k, v in sorted(lista_subfamilia_aux.items(), key=lambda item: item[0])} # ordenando lista de subfamilias
        new_dic[classe][familia] = lista_subfamilia_aux # adicionando subfamilias ordenadas à dict


# 4º Passo
# Escrevendo nova lista em formato tabular +++++++++++++++++++++++++++++++++++
print("Classe\tFamilia\tSubfamilia\tValor") # Cabecalho
for classe in list_classes_ord:
    list_familia = sorted(list(new_dic[classe]))
    quant = list_quants[classe][classe+"_quant"]
    print(classe+"\t\t\t"+quant) # Escreve linha 'classe'
    for familia in list_familia:
        print("\t"+familia+"\t\t"+list_quants[classe][classe+"_"+familia]) # Escreve linha 'familia'
        lista_subf = new_dic[classe][familia]
        subfamilias_list = lista_subf.keys() # Pega valores de subfamilias
        for sub_familia in subfamilias_list: # Para cada subfamilia
            quant = new_dic[classe][familia][sub_familia] # Pega quantidade
            print("\t\t"+sub_familia+"\t"+quant) # Escreve linha 'subfamilia'