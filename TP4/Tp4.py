import sys
import random
import math as m
import copy
import numpy as np


def get_probF_Salida(probF_E, mat_canal):
    pfs = [0, 0]
    for i in range(2):
        pfs[i] = probF_E[0] * mat_canal[0][i] + probF_E[1] * mat_canal[1][i]

    return pfs


def get_prob_condicionales(probF_E, probF_S, mat_canal):
    pcond = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            if probF_S[j] != 0:
                pcond[i][j] = (mat_canal[i][j] * probF_E[i]) / probF_S[j]
    return pcond


def get_entropia_Apriori(probF_E, probF_S):
    entropia_A = 0
    entropia_B = 0

    for p in probF_E:
        if p != 0:
            entropia_A += p * m.log2(1 / p)

    for p in probF_S:
        if p != 0:
            entropia_B += p * m.log2(1 / p)

    return entropia_A, entropia_B


def get_entropia_Aposteriori_A(mat_prob):
    E0 = 0
    E1 = 0
    for i in range(2):
        if mat_prob[i][0] != 0:
            E0 += mat_prob[i][0] * m.log2(1 / mat_prob[i][0])
    for j in range(2):
        if mat_prob[j][1] != 0:
            E1 += mat_prob[j][1] * m.log2(1 / mat_prob[j][1])
    return E0, E1


def get_entropia_Aposteriori_B(mat_prob):
    E0 = 0
    E1 = 0
    for i in range(2):
        if mat_prob[0][i] != 0:
            E0 += mat_prob[0][i] * m.log2(1 / mat_prob[0][i])
    for j in range(2):
        if mat_prob[1][j] != 0:
            E1 += mat_prob[1][j] * m.log2(1 / mat_prob[1][j])
    return E0, E1


def get_prob_suceso_simul(prob_condicionales, probF_S):
    pss = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            pss[i][j] = prob_condicionales[i][j] * probF_S[j]
    return pss


def get_equivocacion(prob_F, entro_Apos_0, entro_Apos_1):
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


def metodoParidadCruzada(mensajes, N, M, flag):
    N = int(N)
    M = int(M)

    if flag == 0:
        paridades = copy.deepcopy(mensajes)
    else:
        mensajes_cortados = [fila[:M] for fila in mensajes[:N]]
        paridades = [list(fila) for fila in mensajes_cortados]

    for i in range(N):
        cant = sum(paridades[i])
        paridades[i].append(0 if cant % 2 == 0 else 1)

    nueva_fila = [0] * (M + 1)
    for j in range(M + 1):
        cant = sum(paridades[i][j] for i in range(N))
        nueva_fila[j] = 0 if cant % 2 == 0 else 1

    paridades.append(nueva_fila)

    return paridades


def enviaMensajes(matriz, mat_canal, flag):
    msn = copy.deepcopy(matriz)
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    for i in range(filas - flag):
        for j in range(columnas - flag):
            x = random.random()
            msn[i][j] = 0 if random.random() <= mat_canal[matriz[i][j]][0] else 1

    return msn


def Get_correctos_incorrectos(matriz_A, matriz_B):
    filas_iguales = 0
    filas_diferentes = 0

    for i in range(len(matriz_A)):
        if matriz_A[i] == matriz_B[i]:
            filas_iguales += 1
        else:
            filas_diferentes += 1
            for j in range(len(matriz_A[i])):
                if matriz_A[i][j] != matriz_B[i][j]:
                    matriz_B[i][j] = matriz_A[i][j]

    return filas_iguales, filas_diferentes, matriz_B


def get_discrepancias_paridades(matriz1, matriz2):
    # Convertir las listas de listas a matrices NumPy
    matriz1 = np.array(matriz1)
    matriz2 = np.array(matriz2)

    Fila1 = matriz1[-1]
    Columna1 = matriz1[:, -1]

    Fila2 = matriz2[-1]
    Columna2 = matriz2[:, -1]

    discrepancias_filas = np.count_nonzero(Fila1 != Fila2)
    discrepancias_columnas = np.count_nonzero(Columna1 != Columna2)

    if discrepancias_filas == 1 & discrepancias_columnas == 1:
        print("Hay un solo error, por ende se corrige")

    elif discrepancias_filas == 0 & discrepancias_columnas == 0:
        print("Los mensajes fueron enviados correctamente")
    else:
        print("Hay mas de un error, imposibilidad de detectarlo y por ende corregirlo")

    return discrepancias_filas, discrepancias_columnas


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

    probF_S = get_probF_Salida(probF_E, mat_canal)

    prob_condicionales = get_prob_condicionales(probF_E, probF_S, mat_canal)

    entropia_Apriori_A, entropia_Apriori_B = get_entropia_Apriori(probF_E, probF_S)

    A_entropia_Aposteriori_0, A_entropia_Aposteriori_1 = get_entropia_Aposteriori_A(
        prob_condicionales
    )
    B_entropia_Aposteriori_0, B_entropia_Aposteriori_1 = get_entropia_Aposteriori_B(
        mat_canal
    )

    prob_suceso_simul = get_prob_suceso_simul(prob_condicionales, probF_S)

    equivocacion_AB = get_equivocacion(
        probF_S, A_entropia_Aposteriori_0, A_entropia_Aposteriori_1
    )

    # H(B/A)
    equivocacion_BA = get_equivocacion(
        probF_E, B_entropia_Aposteriori_0, B_entropia_Aposteriori_1
    )

    # H(A,B)
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
    print("Mensajes a enviar: \n", mensajes)

    if action == "-p":
        Mat_Paridades = metodoParidadCruzada(mensajes, N, M, 0)
        print("Mensajes a enviar + paridades: \n", Mat_Paridades)

        msnRecibido_paridadesViejas = enviaMensajes(Mat_Paridades, mat_canal, 1)
        print("Mensaje recibido + paridades viejas: \n", msnRecibido_paridadesViejas)

        msnRecibido_ParidadesNuevas = metodoParidadCruzada(
            msnRecibido_paridadesViejas, N, M, 1
        )
        print("Mensaje recibido + paridades nuevas: \n", msnRecibido_ParidadesNuevas)
        discrepancias_filas, discrepancias_columnas = get_discrepancias_paridades(
            msnRecibido_paridadesViejas, msnRecibido_ParidadesNuevas
        )
    else:
        msnRecibido = enviaMensajes(mensajes, mat_canal, 0)
        print("Mensaje recibido: \n", msnRecibido)

        correctos, incorrectos, final = Get_correctos_incorrectos(mensajes, msnRecibido)
        print("Mensajes corectos = ", correctos)
        print("Mensajes incorrectos = ", incorrectos)
        print("Mensajes corregidos = ", incorrectos)


if __name__ == "__main__":
    main()
