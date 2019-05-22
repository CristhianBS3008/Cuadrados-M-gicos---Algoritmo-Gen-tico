import random
import math

#Complemento 2 a entero
def comp2ToInt(valor, numeroBits):                                                  #valor debe ser string
    valor = int(valor,2)
    if (valor & (1 << (numeroBits - 1))) != 0:                                      # si el bit de signo es 1
        valor = valor - (1 << numeroBits)                                           # calcula valor negativo
    return valor                                                                    # devuelve valor positivo

#Individuo en binario a Individuo en decimal
def individuoEnDecimal(individuo, ordenMatriz, numeroBitsGen):
    genes=[0 for columna in range(0,ordenMatriz*ordenMatriz)]
    var = ''
    columna = 0
    contador = 0
    for i in range(len(individuo)):
        contador += 1
        var += str(individuo[i])
        if contador == numeroBitsGen:
            valor = comp2ToInt(var,numeroBitsGen)
            genes[columna]=valor
            var = ''
            columna += 1
            contador = 0
    return genes

#Individuo ordenado en una lista, se obtiene individuo ordenado en forma de  matriz nxn, donde n es el ordenMatriz de problema
def vectorToMatriz(individuo):                                                      #individuo debe estar en decimal
    contador = 0
    ordenMatriz = int(math.sqrt(len(individuo)))
    datos = [ [0 for columna in range(0,ordenMatriz)] for fila in range (0,ordenMatriz)]
    for i in range(ordenMatriz):
        for j in range(ordenMatriz):
            datos[i][j]=individuo[contador]
            contador += 1
    return datos

#Devuelve el fitness para cada individuo ingresado
def adaptabilidad(individuo, numDeseado):                                           #individuo en forma matriz nxn
    ordenMatriz = len(individuo[0])                                                 #donde n es el orden de matriz
    fitness = 0
    filas = [0 for columna in range(0,ordenMatriz)]
    columnas = [0 for columna in range(0,ordenMatriz)]
    for i in range(ordenMatriz):
        for j in range(ordenMatriz):
            filas[i] += individuo[i][j]
            columnas[i] += individuo[j][i]

    for i in range(ordenMatriz):                                                    #Cálculo del Fitnees para el problema
        fitness += abs(numDeseado-filas[i]) + abs(numDeseado-columnas[i])

    return fitness

#Genera la Población aleatoria en binario
def generaPoblacion(numeroIndividuos, numeroBits):                                  #numeroBits -> bits que conforman a un individuo
    datos = [ [0 for columna in range(0,numeroBits)] for fila in range (0,numeroIndividuos)]
    for i in range(0,numeroIndividuos):
        for j in range(0,numeroBits):
            datos[i][j] = random.randrange(2)
    return datos

#Transforma la Población en binario a población decimal
def poblacionEnDecimal(poblacion, ordenMatriz, numeroBitsGen):
    numeroIndividuos = len(poblacion)
    poblacionDecimal = [0 for columna in range(numeroIndividuos)]
    for i in range(numeroIndividuos):
        poblacionDecimal[i]= individuoEnDecimal(poblacion[i], ordenMatriz, numeroBitsGen)
    return poblacionDecimal

#teniendo la población en decimal saca el fitness para cada individuo de la población
def poblacionFitness(poblacionDecimal, numDeseado):
    numeroIndividuos = len(poblacionDecimal)
    poblacionFit = [0 for columna in range(numeroIndividuos)]
    for i in range(numeroIndividuos):
        individuoEnMatriz = vectorToMatriz(poblacionDecimal[i])
        poblacionFit[i]= adaptabilidad(individuoEnMatriz, numDeseado)
    return poblacionFit

#Evaluando el fitnees de cada individuo, se procede a reemplazar al peor y emparejar de manera aleatoria
def generaParejas(poblacionFitness, poblacion, numBitsIndividuo):
    #Se reemplaza al mejor individuo por el peor individuo
    posMejor = poblacionFitness.index(min(poblacionFitness))
    posPeor = poblacionFitness.index(max(poblacionFitness))
    poblacionRespaldo = list(poblacion)
    poblacionRespaldo[posPeor] = poblacion[posMejor]

    #Se empareja a los individuos de manera aleatoria
    indices = []
    for i in range(len(poblacionFitness)):
        indices.append(i)
    random.shuffle(indices)
    
    contador = 0
    poblacionFinal = list(poblacionRespaldo)
    for i in indices:
        poblacionFinal[contador]=poblacionRespaldo[i]
        contador += 1
    return poblacionFinal       #devuelve lista de bits, tamaño = numBitsIndividuo*numIndividuos

#Teniendo el número de cortes, se procede a establecer pts de cortes de manera aleatoria, para el crossover
def crossover(puntosCross, poblacion):      #la población debe estar en bits y emparejada
    poblacionFinal = list(poblacion)
    numBitsIndividuo = len(poblacion[0])

    #Una vez establecido los pts crossover aleatoriamente, se cruza las parejas
    for x in range(len(poblacion)):
        if x%2 == 1:                        #agarramos la pos 1,3,5,... del vectorPuntos. para tener dos elementos siempre
            vectorPuntos=[0 for columna in range(puntosCross)]
            for i in range(puntosCross):
                vectorPuntos[i]=random.randint(0,numBitsIndividuo-2) # es -2 pq no cojo último bit para ptos aleatorios crossover
            vectorPuntos.append(numBitsIndividuo-1)                 #agrego como pto crossover al último bit        
            vectorPuntos = sorted(vectorPuntos)
            poblacionFinal[x-1],poblacionFinal[x] = cruce(vectorPuntos, poblacion[x-1],poblacion[x])     #si la matriz tiene num de elemnt impares, entonces el ult elemento no se empareja con nadie
    
    return poblacionFinal       #devuelve lista de bits

#Subfunción de genetic.crossover, genera el crossover para dos individuos escojidos con sus respectivos pts crossover
def cruce(vectorPuntos, individuo1, individuo2):
    individuo1Final = list(individuo1)
    individuo2Final = list(individuo2)
    for i in range(len(vectorPuntos)):              #i = 0 1 2 3 4 . . . .
        if i%2 == 1:                                # --> 1 3 . . . .     -->> mismo efecto anterior, escojo solo parejas de puntos
            for j in range(vectorPuntos[i-1],vectorPuntos[i]+1):    # +1 en caso se repitan los mismo pts para el crossover
                individuo1Final[j] = individuo2[j]
                individuo2Final[j] = individuo1[j]

    return individuo1Final,individuo2Final

#Según el factor de mutación se establece la probabilidad de mutación, según numeroBitsMutados se establece cuántos bits
#mutarán de cada individuo
def mutacion(factorMutacion, numeroBitsMutados,poblacion):      #poblacion en bits
    suerte = random.randrange(factorMutacion)
    poblacionMutada = list(poblacion)
    numeroBitsIndividuo = len(poblacion[0])
    if suerte == 0:
        for i in range(len(poblacion)):
            posicionBit = [0 for columna in range(numeroBitsMutados)]
            for k in range(numeroBitsMutados):
                posicionBit[k]=random.randrange(numeroBitsIndividuo)

            for j in posicionBit:
                if poblacion[i][j] == 1:
                    poblacionMutada[i][j] = 0
                else:
                    poblacionMutada[i][j] = 1


    return poblacionMutada                                      #devuelve lista población en bits