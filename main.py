import tools.report as rep
import extra_lib.metamodel as mmodel
import random

# As próximas cinco linhas referem-se à criação, ajuste e treinamento da rede neural que
# serve como metamodelo para este problema. Sua operação de predição será o nosso fitness
print(
    "Matias Vargas Maekawa Fernandes Moraes e Silva (MVMFMS) é um diretor de hospital que visa atender o máximo de pacientes possível em sua unidade hospitalar.")
print("Para isso, ele precisa saber quantos funcionarios ele deverá contratar e qual o seu ganho com isso.")
print(
    "A sua equipe técnica projetou uma solução que toma a quantidade de recepcionistas, técnicos, médicos, enfermeiras na sala de tratamento e enfermeiras na sala de emergência, sendo representadas respectivamente pelas variáveis x1, x2, x3, x4, x5.")
print("Este problema é baseado em um caso real definido no trabalho de Ahmed e Alkhamis (2009).")
print("Será agora instanciado um metamodelo, baseado em redes neurais, que consome um dataset coletado para este caso.")
print(
    "Em seguida, o algoritmo genético desenvolvido deverá maximizar as entradas a fim de definir os melhores valores possíveis para cada variável.")

print()
print("Pressione 1 para continuar e 0 para abortar")
print()
segue = int(input())


if (segue == 1):
    rep.write_text('-------------------------------------- Instanciando o metamodelo --------------------------------------')
    test = mmodel.metamodel()
    test.cuda_status()
    test.fit()
    test.train_performance()
    test.model_peformance()


# Instanciação das variáveis globais principais
best = -100000
high_bound = 12  # Limite superior, útil para estimar as gerações
populations = ([[random.randint(1, 12) for x in range(5)] for i in range(4)])  # População inicial
parents = []  # Pais nos crossovers
melhores_scores = []  # Eleição dos melhores fitness
melhores_cromossomos = []  # Eleição dos melhores cromossomos
crossover_results = []  # Resultado dos crossovers


def generations():
    return high_bound ** 3  # Estima uma quantidade suficientemente boa para a quantidade de gerações


def fitness_score():  # Aqui são eleitos os cromossomos com os melhores desempenhos de sua geração
    global populations, best, melhores_scores, melhores_cromossomos
    fit_value = []
    rep.write_text()
    for i in range(len(populations)):
        fit_value.append(
            test.predict(populations[i]))  # Aqui é aplicada a predição com cada um dos cromossomos da população.
        # Seu resultado é guardado em uma lista

    rep.write_text(f'Valores de fitness: {fit_value}')
    rep.write_text()
    fit_value, populations = zip(*sorted(zip(fit_value, populations),
                                         reverse=True))  # Associa-se os melhores cromossomos aos seus scores, ordenado pelo score
    best = fit_value[0]  # Variável que guarda o melhor desempenho da geração
    rep.write_text(
        f'População ordenada por score: {populations}')  # População ordenada pelo score, do melhor ao pior. Esse esquema será base para o crossover

    melhores_scores.append(best)  # Guardam os scores ordenados
    melhores_cromossomos.append(populations[0])  # Guarda o melhor cromossomo da geração


def selectparent():  # Escolhem-se os pais
    global parents, populations
    parents.clear()
    # Nesse esquema, por ser uma população para, então fecham-se casais
    # O crossover se dá pelo cruzamento do melhor com o pior, do segundo melhor com o segundo pior

    parents.append(populations[0])
    parents.append(populations[3])
    parents.append(populations[1])
    parents.append(populations[2])
    rep.write_text(f'Casais formados {parents}')
    rep.write_text()


def crossover():
    global parents, crossover_results, populations
    cross_point = 2  # Ponto de corte no cromossomo
    crossover_results.clear()
    # Para formar novos filhos, pega-se a primeira metade da mãe e junta com a segunda metade do pai
    # O segundo filho, pegam as metades inversas, até serem formados 4 novos filhos, que
    # Irão substituir por completo a geração anterior, sem elitismo
    crossover_results.append(parents[0][0:cross_point + 1] + parents[1][cross_point + 1:])
    crossover_results.append(parents[0][cross_point + 1:] + parents[1][0:cross_point + 1])
    crossover_results.append(parents[2][0:cross_point + 1] + parents[3][cross_point + 1:])
    crossover_results.append(parents[2][cross_point + 1:] + parents[3][0:cross_point + 1])

    rep.write_text()
    rep.write_text(f'Crossover feito: {crossover_results}')


def mutation():
    global populations, crossover_results
    # O esquema de mutação funciona como um ajuste do crossover
    # Apelidado aqui de "correção genética", a mutação anda de gene em gene verificando se
    # O limite superior está correto. Caso não esteja, um novo valor, dentro do seu respectivo
    # limite é sorteado, permitindo que a regra dos limites seja mantida

    for i in range(4):
        for x in range(5):
            if (x == 0 and (crossover_results[i][x] not in range(1, 3))):
                crossover_results[i][x] = random.randint(2, 3)

            if (x == 1 and (crossover_results[i][x] not in range(1, 4))):
                crossover_results[i][x] = random.randint(3, 4)

            if (x == 2 and (crossover_results[i][x] not in range(1, 5))):
                crossover_results[i][x] = random.randint(4, 5)

            if (x == 3 and (crossover_results[i][x] not in range(1, 6))):
                crossover_results[i][x] = random.randint(5, 6)

            if (x == 4 and (crossover_results[i][x] not in range(1, 12))):
                crossover_results[i][x] = random.randint(6, 12)

    populations = crossover_results
    rep.write_text()
    rep.write_text(f'População pós-mutação: {populations}')


def ajusta_populacao():
    global populations
    for i in range(4):
        for x in range(5):
            if (x == 0):
                populations[i][x] = random.randint(1, 3)
            if (x == 1):
                populations[i][x] = random.randint(2, 4)
            if (x == 2):
                populations[i][x] = random.randint(3, 5)
            if (x == 3):
                populations[i][x] = random.randint(4, 6)
            if (x == 4):
                populations[i][x] = random.randint(10, 12)


if (segue == 1):
    rep.clear_report()
    M = generations()
    ajusta_populacao()  # O ajuste aqui serve para corrigir falhas que possa ter ocorrido na criação
    # da população inicial, em função dos limites superiores de cada variável
    for i in range(M):
        rep.write_text()
        rep.write_text()
        rep.write_text(
            f'-------------------------------------- Iniciando o AG, geração {i} --------------------------------------')
        rep.write_text()
        rep.write_text()
        rep.write_text(f'População inicial da geração {i}: {populations}')
        rep.write_text()
        rep.write_text('-------------------------------------- Aplicando o fitness --------------------------------------')
        fitness_score()
        rep.write_text()
        rep.write_text('-------------------------------------- Selecionando os pais --------------------------------------')
        selectparent()
        rep.write_text()
        rep.write_text('-------------------------------------- Aplicando o crossover --------------------------------------')
        rep.write_text()
        crossover()
        rep.write_text('-------------------------------------- Aplicando a mutação --------------------------------------')
        mutation()
        rep.write_text()

    rep.write_text()
    # Informa para o usuário os resultados
    melhores_scores, melhores_cromossomos = zip(*sorted(zip(melhores_scores, melhores_cromossomos), reverse=True))
    rep.write_text(f'Melhor fitness {melhores_scores[0]}')
    rep.write_text()
    rep.write_text(f'Melhor cromossomo {melhores_cromossomos[0]}')
    rep.write_text()
