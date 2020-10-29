import os
import sys

#  comando válido -> python3 copy_limit_lines.py arquivoAserCopiado.txt output.txt 10

localArquivoAserCopiado = sys.argv[1]
limiteLinhas = int(sys.argv[2])
nomeArquivoSaida = sys.argv[3]
os.system("rm "+nomeArquivoSaida)

contadorLinhas = 0

with open(localArquivoAserCopiado, "r") as arquivoLeitura:

    for linha in arquivoLeitura:   
        contadorLinhas += 1
        with open(nomeArquivoSaida, "a+") as novoArq:
            novoArq.write(linha)

        if contadorLinhas == limiteLinhas:
            break

    print("Arquivo copiado com " + str(limiteLinhas) + " linhas !")