import sys
import random
import math as m
import copy


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
            entropia_A += p * m.log(1 / p)

    for p in probF_S:
        if p != 0:
            entropia_B += p * m.log(1 / p)

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
    Hab = 0
    for i in range(2):
        for j in range(2):
            if prob_condicionales[i][j] != 0:
                Hab += prob_suceso_simul[i][j] * m.log(1 / prob_condicionales[i][j])
    return Hab


def generaMensajes(N, M, probF_E):
    msn = [[0 for _ in range(len(M))] for _ in range(len(N))]
    for i in range(len(N)):
        for j in range(len(M)):
            msn[i][j] = 0 if random.random() <= probF_E[0] else 1
    return msn


def metodoParidadCruzada(mensajes, N, M):
    paridades = copy.deepcopy(mensajes)
    N = int(N)
    M = int(M)
    for i in range(N):
        cant = 0
        for j in range(M):
            cant += paridades[i][j]
        if cant % 2 == 0:
            paridades[i].append(0)
        else:
            paridades[i].append(1)

    for j in range(M):
        cant = sum(paridades[i][j] for i in range(N))
        if cant % 2 == 0:
            paridades.append([0])
        else:
            paridades.append([1])

    return paridades


def enviaMensajes(matriz, mat_canal):
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    msn = []
    for i in range(filas):
        for j in range(columnas):
            x = random.random()
            msn[i][j] = 0 if random.random() <= mat_canal[matriz[i][j]][0] else 1
    return msn


def main():
    args = sys.argv

    # tpi4 probs.txt N M [-p]
    if len(args) > 7 or len(args) < 4:
        print("Uso: tpi4 probs.txt N M [-p]")
        sys.exit(1)

    arch = args[2]
    N = args[3]
    M = args[4]
    action = args[5]

    mat_canal = []

    probF_E = [0, 0]

    #!a chequear
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

    # H(A) , H(B)
    entropia_Apriori_A, entropia_Apriori_B = calc_entropia_Apriori(probF_E, probF_S)

    # H(A/b=0) , H(A/b=1)  #! tmb con B?
    entropia_Aposteriori_0, entropia_Aposteriori_1 = calc_entropia_Aposteriori(
        probF_E, mat_canal, prob_condicionales
    )

    # P(ai,bi)
    prob_suceso_simul = cal_prob_suceso_simul(prob_condicionales, probF_S)

    # H(A/B) #! tmb con B?
    equivocacion = calc_equivocacion(prob_suceso_simul, prob_condicionales)

    # I(A,B) = I (B,A)
    info_mutua = entropia_Apriori_A - equivocacion

    print("MATRIZ DEL CANAL: \n", mat_canal)
    print("PROBABILIDAD DE LA FUENTE DE ENTRADA P(ai): ", probF_E)
    print("PROBABILIDAD DE LA FUENTE DE SALIDA P(bi): ", probF_S)
    print("PROBABILIDAD DE SUCESO SIMULTANEO P(ai,bi): \n ", prob_suceso_simul),

    print("PROBABILIDAD CONDICIONAL P(ai/bi):", prob_condicionales)
    print(
        "ENTROPIA APRIORI: H(A) = {}   H(B) = {}".format(
            entropia_Apriori_A, entropia_Apriori_B
        )
    )
    print(
        "ENTROPIA APOSTERIORI: H(A/b=0) = {}   H(A/b=1)= {}".format(
            entropia_Aposteriori_0, entropia_Aposteriori_1
        )
    )
    print("EQUIVOCACION: H(A/B) = ", equivocacion)
    print("INFORMACION MUTUA: I(A,B) = ", info_mutua)

    mensajes = generaMensajes(N, M, probF_E)

    if action == "-p":
        Mat_Paridades = metodoParidadCruzada(mensajes, N, M)
        msnEnviado = enviaMensajes(Mat_Paridades, mat_canal)
        print("MENSAJES A ENVIAR CON PARIDADES: ", Mat_Paridades)
    else:
        msnEnviado = enviaMensajes(mensajes, mat_canal)
        print("MENSAJES A ENVIAR: ", mensajes)

    print("MENSAJE ENVIADO: ", msnEnviado)


if __name__ == "__main__":
    main()
