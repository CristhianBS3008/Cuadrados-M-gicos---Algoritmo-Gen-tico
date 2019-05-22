import genetic

N_INDIVIDUOS = 12
ORDEN_MATRIZ = 9
BITS_GEN = 9
N_BITS = ORDEN_MATRIZ*ORDEN_MATRIZ*BITS_GEN         #Numero Bits por Individuo
MAX_NUM_ITER = 10000
OBJETIVO = 45
PUNTOS_CROSSOVER = 30
NUM_BITS_MUTADOS = 1
FACTOR_MUTACION = 9         #  es el (1/FACTOR_MUTACION)*100% de probabilidad para mutar
                            #  el fitness mejorará más rápido si se tiene mayor valor en PUNTOS_CROSSOVER
                            #  pero esto generará mediocridad o mejor dicho, no mejorarimiento de los hijos con respecto a los padres
                            #  Esto se soluciona con la mutación, si el factor de mutación es muy bajo, generará inestabilidad
                            #  y mutará muchos hijos con malos fitness, empeorando la población
                            #  si el factor de mutación es muy alto, durante muchas generaciones se observará mediocridad

iter = 0

poblacion = genetic.generaPoblacion(N_INDIVIDUOS,N_BITS)
#print(poblacion)

while iter < MAX_NUM_ITER:
    print('Generación Numero: ',iter)

    poblacionDecimal = genetic.poblacionEnDecimal(poblacion, ORDEN_MATRIZ, BITS_GEN)
    #print(poblacionDecimal)

    poblacionFit = genetic.poblacionFitness(poblacionDecimal, OBJETIVO)
    print('Fitness de la Poblacion: ',poblacionFit)

    poblacionEmparejada = genetic.generaParejas(poblacionFit, poblacion, N_BITS)
    #print(poblacionEmparejada)

    poblacionCruzada = genetic.crossover(PUNTOS_CROSSOVER,poblacionEmparejada)
    #print(poblacionCruzada)

    poblacionNueva = genetic.mutacion(FACTOR_MUTACION,NUM_BITS_MUTADOS,poblacionCruzada)
    #print(poblacionNueva)

    poblacion = poblacionNueva

    print('Mejor fitness: ', min(poblacionFit))
    print('Peor fitness: ', max(poblacionFit))
    promedio = sum(poblacionFit)/len(poblacionFit)
    print('Promedio: ',promedio)

    if min(poblacionFit) == 0:
        posicion = poblacionFit.index(min(poblacionFit))
        individuoEnMatriz = genetic.vectorToMatriz(poblacionDecimal[posicion])
        print('Matriz Solución:  ')
        for i in range(len(individuoEnMatriz)):
            print(individuoEnMatriz[i])
        break

    print("""
            """)

    iter += 1