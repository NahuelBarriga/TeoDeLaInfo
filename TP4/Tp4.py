import sys
import random
import math as m
import copy
import numpy as np


def calc_probF_Salida(probF_E, mat_canal):
    pfs = [0, 0]
    for i in range(2):
        pfs[i] = probF_E[0] * mat_canal[0][i] + probF_E[1] * mat_canal[1][i]

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
            entropia_A += p * m.log2(1 / p)

    for p in probF_S:
        if p != 0:
            entropia_B += p * m.log2(1 / p)

    return entropia_A, entropia_B


def calc_entropia_Aposteriori_A(mat_prob):
    E0 = 0
    E1 = 0
    for i in range(2):
        if mat_prob[i][0] != 0:
            E0 += mat_prob[i][0] * m.log2(1 / mat_prob[i][0])
    for j in range(2):
        if mat_prob[j][1] != 0:
            E1 += mat_prob[j][1] * m.log2(1 / mat_prob[j][1])
    return E0, E1


def calc_entropia_Aposteriori_B(mat_prob):
    E0 = 0
    E1 = 0
    for i in range(2):
        if mat_prob[0][i] != 0:
            E0 += mat_prob[0][i] * m.log2(1 / mat_prob[0][i])
    for j in range(2):
        if mat_prob[1][j] != 0:
            E1 += mat_prob[1][j] * m.log2(1 / mat_prob[1][j])
    return E0, E1


def cal_prob_suceso_simul(prob_condicionales, probF_S):
    pss = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            pss[i][j] = prob_condicionales[i][j] * probF_S[j]
    return pss


def calc_equivocacion(prob_F, entro_Apos_0, entro_Apos_1):
    equi = prob_F[0] * entro_Apos_0 + prob_F[1] * entro_Apos_1
    return equi


def generaMensajes(N, M, probF_E):
    N = int(N)
    M = int(M)
    msn = [[0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            msn[i][j] = 0 if random.random() <= probF_E[0] else 1
    return msn


def metodoParidadCruzada(mensajes, N, M):
    paridades = copy.deepcopy(mensajes)
    N = int(N)
    M = int(M)

    for i in range(N):
        cant = sum(paridades[i][j] for j in range(M))
        paridades[i].append(0 if cant % 2 == 0 else 1)

    paridad_columna = sum(paridades[i][-1] for i in range(N))
    paridades.append([0 if paridad_columna % 2 == 0 else 1] * (M + 1))

    return paridades


def enviaMensajes(matriz, mat_canal):
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    msn = []

    for _ in range(filas):
        msn.append([0] * columnas)

    for i in range(filas):
        for j in range(columnas):
            x = random.random()
            msn[i][j] = 0 if random.random() <= mat_canal[matriz[i][j]][0] else 1
    return msn


def msnErroneos(mat_1, mat_2):
    matriz_a = np.array(mat_1)
    matriz_b = np.array(mat_2)

    for i in range(len(matriz_a)):
        if not np.array_equal(matriz_a[i], matriz_b[i]):
            return i

    # Si todas las filas son iguales, devuelve -1 para indicar que no hay diferencias
    return -1


def main():
    args = sys.argv

    # tpi4 probs.txt N M [-p]
    if len(args) > 7 or len(args) < 4:
        print("Uso: tpi4 probs.txt N M [-p]")
        sys.exit(1)

    arch = args[2]
    N = args[3]
    M = args[4]
    if len(args) == 6:
        action = args[5]
    else:
        action = ""

    mat_canal = []
    probF_E = []

    with open("Samples/" + arch, "r") as f:
        for i, linea in enumerate(f):
            valores = list(map(float, linea.split()))
            if i == 0:
                probF_E = valores
            elif 1 <= i <= 2:
                mat_canal.append(valores)

    # P(bi)
    probF_S = calc_probF_Salida(probF_E, mat_canal)

    # P(ai/bi)
    prob_condicionales = calc_prob_condicionales(probF_E, probF_S, mat_canal)

    # H(A), H(B)
    entropia_Apriori_A, entropia_Apriori_B = calc_entropia_Apriori(probF_E, probF_S)

    # H(A/b=0), H(A/b=1)  #! tmb con B?
    A_entropia_Aposteriori_0, A_entropia_Aposteriori_1 = calc_entropia_Aposteriori_A(
        prob_condicionales
    )

    # H(B/a=0),  H(B/a=1)
    B_entropia_Aposteriori_0, B_entropia_Aposteriori_1 = calc_entropia_Aposteriori_B(
        mat_canal
    )

    # P(ai,bi)
    prob_suceso_simul = cal_prob_suceso_simul(prob_condicionales, probF_S)

    # H(A/B)
    equivocacion_AB = calc_equivocacion(
        probF_S, A_entropia_Aposteriori_0, A_entropia_Aposteriori_1
    )

    # H(B/A)
    equivocacion_BA = calc_equivocacion(
        probF_E, B_entropia_Aposteriori_0, B_entropia_Aposteriori_1
    )

    # H(A,B)
    print("AAAAA", entropia_Apriori_A, equivocacion_BA)
    entropia_Afin = entropia_Apriori_A + equivocacion_BA

    # I(A,B) = I (B,A)
    info_mutuaAB = entropia_Apriori_A - equivocacion_AB
    info_mutuaBA = entropia_Apriori_B - equivocacion_BA

    print("Matriz del canal:  \n", mat_canal)
    print("Probabilidad de la fuente de entrada P(ai): \n", probF_E)
    print("Probabilidad de la salida P(bi):  \n", probF_S)
    print("Probabilidad del suceso simultaneo P(ai,bi):  \n", prob_suceso_simul)

    print("Probabilidad condicional P(ai/bi): \n", prob_condicionales)
    print("Entropia Apriori: ")
    print(
        "     H(A) = {:.3f}       H(B) = {:.3f}".format(
            entropia_Apriori_A, entropia_Apriori_B
        )
    )
    print("Entropia Aposteriori: ")
    print(
        "     H(A/b=0) = {:.3f}   H(A/b=1)= {:.3f}".format(
            A_entropia_Aposteriori_0, A_entropia_Aposteriori_1
        )
    )
    print(
        "     H(B/a=0) = {:.3f}   H(B/a=1)= {:.3f}".format(
            B_entropia_Aposteriori_0, B_entropia_Aposteriori_1
        )
    )
    print("Equivocacion: ")
    print(
        "     H(A/B) =  {:.3f}    H(B/A) =  {:.3f} ".format(
            equivocacion_AB, equivocacion_BA
        )
    )
    print("Entropia Afin:  ")
    print("     H(A,B) =  {:.3F}".format(entropia_Afin))
    print("Informacion mutua: ")
    print("     I(A,B) =  {:.3f}   I(B,A) =  {:.3f}".format(info_mutuaAB, info_mutuaBA))

    mensajes = generaMensajes(N, M, probF_E)

    if action == "-p":
        Mat_Paridades = metodoParidadCruzada(mensajes, N, M)
        msnEnviado = enviaMensajes(Mat_Paridades, mat_canal)
        print("MENSAJES A ENVIAR CON PARIDADES: ", Mat_Paridades)
    else:
        msnEnviado = enviaMensajes(mensajes, mat_canal)
        print("MENSAJES A ENVIAR: ", mensajes)

    print("MENSAJE ENVIADO: ", msnEnviado)

    print("CANTIDAD DE MENSAJES INCORRECTOS")
    print("CANTIDAD DE MENSAJES CORREGIDOS")


if __name__ == "__main__":
    main()
