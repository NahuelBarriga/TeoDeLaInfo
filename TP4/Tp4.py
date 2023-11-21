import sys
import random
import math as m


def imprimirMatriz(matriz):
    for fila in matriz:
        print(fila)


def calc_probF_Salida(probF_E, mat_canal):
    pfs = [0, 0]
    for i in range(2):
        pfs[i] = probF_E[i] * mat_canal[i][0] + probF_E[1] * mat_canal[i][1]
    return pfs


def calc_prob_condicionales(probF_E, probF_S, mat_canal):
    pcond = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            if probF_S[j] != 0:
                pcond[i][j] = (mat_canal[i][j] * probF_E[i]) / probF_S[j]
    return pcond


def calc_entropia_Apriori(probF_E, probF_S):
    entropia_A = 0
    entropia_B = 0

    for p in probF_E:
        if p != 0:
            entropia_A += p * math.log(1 / p)

    for p in probF_S:
        if p != 0:
            entropia_B += p * math.log(1 / p)

    return entropia_A, entropia_B


def calc_entropia_Aposteriori(probF, mat_canal, prob_condicionales):
    E0 = 0
    E1 = 0
    for i in range(2):
        if prob_condicionales[0][i] != 0:
            E0 += prob_condicionales[0][i] * m.log(1 / prob_condicionales[0][i])
    for j in range(2):
        if prob_condicionales[1][j] != 0:
            E1 += prob_condicionales[1][j] * m.log(1 / prob_condicionales[1][j])
    return E0, E1


def cal_prob_suceso_simul(prob_condicionales, probF_S):
    pss = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            pss[i][j] = prob_condicionales[i][j] * probF_S[j]
    return pss


def calc_equivocacion(prob_suceso_simul, prob_condicionales):
    for i in range(2):
        for j in range(2):
            if prob_condicionales[i][j] != 0:
                Hab += prob_suceso_simul[i][j] * m.log(1 / prob_condicionales[i][j])
    return equi


def generaMensajes(N, M, probF_E):
    msn = [[0 for _ in range(len(M))] for _ in range(len(N))]

    for i in range(len(N)):
        for j in range(len(M)):
            msn[i][j] = 0 if random.random() <= probF_E[0] else 1

    return msn


def metodoParidadCruzada(mensajes, N, M):
    paridades = copy.deepcopy(mensajes)

    for i in N:
        cant = sum(paridades[i][j] for j in M)
        if cant % 2 == 0:
            paridades[i][M] = 0
        else:
            paridades[i][M] = 1

    for j in M:
        cant = sum(paridades[i][j] for i in N)
        if cant % 2 == 0:
            paridades[N][j] = 0
        else:
            paridades[N][j] = 1

    return paridades


def enviaMensajes(matriz, mat_canal):
    msn = []
    for i in N:
        for j in M:
            x = random.random()
            msn[i][j] = 0 if random.random() <= mat_canal[matriz[i][j]][0] else 1
    return msn


def main():
    args = sys.argv

    # tpi4 probs.txt N M [-p]
    print("len(Args)", len(args))
    if len(args) > 7 or len(args) < 4:
        print("Uso: tpi4 probs.txt N M [-p]")
        sys.exit(1)

    arch = args[2]
    N = args[3]
    M = args[4]
    action = args[5]
    print("action", action)
    mat_canal = [[0, 0], [0, 0]]
    # P(ai)
    probF_E = [0, 0]

    #!a chequear
    with open("Samples/" + arch, "r") as f:
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

    # H(A) , H(B)
    entropia_Apriori_A, entropia_Apriori_B = calc_entropia_Apriori(probF_E, probF_S)

    # H(A/b=0) , H(A/b=1)  #! tmb con B?
    entropia_Aposteriori_0, entropia_Aposteriori_1 = calc_entropia_Aposteriori(
        probF, mat_canal, prob_condicionales
    )

    # P(ai,bi)
    prob_suceso_simul = cal_prob_suceso_simul(prob_condicionales, probF_S)

    # H(A/B) #! tmb con B?
    equivocacion = calc_equivocacion(prob_suceso_simul, prob_condicionales)

    # I(A,B) = I (B,A)
    info_mutua = entropia_Apriori - equivocacion

    print("MATRIZ DEL CANAL:", imprimirMatriz(mat_canal))
    print("PROBABILIDAD DE LA FUENTE DE ENTRADA P(ai):", probFE)
    print("PROBABILIDAD DE LA FUENTE DE SALIDA P(bi):", probF_S)
    print("PROBABILIDAD DE SUCESO SIMULTANEO P(ai,bi): ",imprimirMatriz(prob_suceso_simul))
    print("PROBABILIDAD CONDICIONAL P(ai/bi):", imprimirMatriz(prob_condicionales))
    print("ENTROPIA APRIORI: H(A) = {}   H(B) = {}".format(entropia_Apriori_A, entropia_Apriori_B))
    print("ENTROPIA APOSTERIORI: H(A/b=0) = {}   H(A/b=1)= {}".format(entropia_Aposteriori_0, entropia_Aposteriori_1))
    print("EQUIVOCACION: H(A/B) = ", equivocacion)
    print("INFORMACION MUTUA: I(A,B) = ", info_mutua)

    mensajes = generaMensajes(N, M, probF_E)

    if action == "-p":
        Mat_Paridades = metodoParidadCruzada(mensajes, N, M)
        msnEnviado = enviaMensajes(Mat_Paridades, mat_canal)
        print("MENSAJES A ENVIAR CON PARIDADES: ", imprimirMatriz(Mat_Paridades))
    else:
        msnEnviado = enviaMensajes(mensajes, mat_canal)
        print("MENSAJES A ENVIAR: ", imprimirMatriz(mensajes))

    print("MENSAJE ENVIADO:", imprimirMatriz(msnEnviado))


if __name__ == "__main__":
    main()
