import sys
import random
import math as m


def calc_probF_Salida(probF_E, mat_canal):
    pfs = []
    for i in 1:
        pfs[i] = probF_E[i] * mat_canal[i][0] + probF_E[1] * mat_canal[i][1]
    return pfs


def calc_prob_condicionales(probF_E, probF_S, mat_canal):
    pcond = []
    for i in 1:
        for j in 1:
            if probF_S[j] != 0:
                pcond[i][j] = (mat_canal[i][j] * probF_E[i]) / probF_S[j]
    return pcond


def calc_entropia_Apriori(probF_E, probF_S):
    entropia_A = sum(p * m.log(1 / p) for p in probF_E)
    entropia_B = sum(p * m.log(1 / p) for p in probF_S)
    return entropia_A, entropia_B


def calc_entropia_Aposteriori(probF, mat_canal, prob_condicionales):
    for i, j in 1:
        if prob_condicionales[0][i] != 0:
            E0 += prob_condicionales[0][i] * m.log(1 / prob_condicionales[0][i])
    for j in 1:
        if prob_condicionales[1][i] != 0:
            E1 += prob_condicionales[1][i] * m.log(1 / prob_condicionales[1][i])
    return E0, E1


def cal_prob_suceso_simul(prob_condicionales, probF_S):
    for i in 1:
        for j in 1:
            pss[i][j] = prob_condicionales[i][j] * probF_S[j]
    return pss


def calc_equivocacion(prob_suceso_simul, prob_condicionales):
    for i in 1:
        for j in 1:
            if prob_condicionales[i][j] != 0:
                Hab += prob_suceso_simul[i][j] * m.log(1 / prob_condicionales[i][j])
    return equi


def generaMensajes(N, M, probF_E):
    msn = []
    for i in N:
        for j in M:
            x = random.random()
            if x <= probF_E[0]:
                msn[i][j] = 0
            else:
                msn[i][j] = 1
    return msn


def main():
    args = sys.argv

    # tpi4 probs.txt N M [-p]
    if len(args) > 5 or len(args) < 4:
        print("Uso: tpi4 probs.txt N M [-p]")
        sys.exit(1)

    arch = arg[1]
    N = arg[2]
    M = arg[3]
    action = arg[5]

    mat_canal = []
    # P(ai)
    probF_E = []

    #!a chequear
    with open("Samples/" + original_file, "r") as f:
        for i, linea in enumerate(f):
            valores = list(map(float, linea.split()))
            if i == 0:
                probF = valores
            elif i == 1 or i == 2:
                mat_canal.append(valores)

    # P(bi)
    probF_S = calc_probF_Salida(probF_E, mat_canal)

    # P(ai/bi)
    prob_condicionales = calc_prob_condicionales(probF_E, probF_S, mat_canal)

    # H(A)
    entropia_Apriori_A, entropia_Apriori_B = calc_entropia_Apriori(probF_E, probF_S)
    # H(A/b=0) , H(A/b=1)  #! tmb con B?
    entropia_Aposteriori_0, entropia_Aposteriori_1 = calc_entropia_Aposteriori(
        probF_E, probF_S
    )

    # P(ai,bi)
    prob_suceso_simul = cal_prob_suceso_simul(prob_condicionales, probF_S)

    # H(A/B) #! tmb con B?
    equivocacion = calc_equivocacion(prob_suceso_simul, prob_condicionales)

    # I(A,B)
    info_mutua = entropia_Apriori - equivocacion

    #! a chequear: supuestamente hay q pasar cada mensaje por la matriz del canal, para q? como?
    mensajes = generaMensajes(N, M, probF_E)

    #! paridad cruzada criterio par = 0 si la suma de ceros de vrc y lrc es par ?
    if action == "-p":
        Mat_Paridades = metodoParidadCruzada(mat_canal, mensajes)

    print("probFE:", probFE)
    print("Matriz:", matriz)


if __name__ == "__main__":
    main()
