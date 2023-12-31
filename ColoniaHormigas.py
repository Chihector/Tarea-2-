import sys
import pandas as pd
import numpy as np

# Función para calcular la matriz de distancias entre ciudades
def obtenerDistancias(numVar, matriz):
    matrizDistancias = np.full((numVar, numVar), fill_value=-1.0, dtype=float)

    for i in range(numVar - 1):
        for j in range(i + 1, numVar):
            distancia = np.sqrt(np.sum(np.square(matriz[i] - matriz[j])))
            matrizDistancias[i][j] = distancia
            matrizDistancias[j][i] = distancia

    return matrizDistancias

# Función para calcular la matriz de heurísticas
def obtenerHeuristicas(matriz):
    matrizHeuristicas = np.full_like(matriz, fill_value=(1 / matriz), dtype=float)
    np.fill_diagonal(matrizHeuristicas, 0.0)

    return matrizHeuristicas

# Función para inicializar la matriz de feromonas
def obtenerFeromonas(matriz, numVar, mejorCosto):
    matrizFeromonas = np.full_like(matriz, 1 / (mejorCosto * numVar))

    return matrizFeromonas

# Función para calcular el costo de una solución
def solucionCalcularCosto(cantNodos, matrizSolucion, matrizBase):
    costo = matrizBase[matrizSolucion[-1]][matrizSolucion[0]]
    for i in range(cantNodos - 1):
        costo += matrizBase[matrizSolucion[i]][matrizSolucion[i + 1]]
    return costo

# Función para inicializar hormigas en posiciones aleatorias
def inicializarHormigas(hormiga, nodos):
    poblacion = np.full((hormiga, nodos), -1)
    for i in range(hormiga):
        poblacion[i][0] = float(np.random.randint(nodos))

    return poblacion

# Función para seleccionar el siguiente segmento de la ruta
def seleccionarNuevoSegmento(nodos, tamañoPobl, pobl, feromona, feromLocal, probLim, matrizDistancias, valorHeur, factorEvapFerom):
    matrizNodos = np.arange(nodos)
    for i in range(tamañoPobl):
        row = pobl[i][:]
        nodosVisitados = np.where(row != -1)
        nodosVisitados = [pobl[i][item] for item in nodosVisitados]
        nodosNoVisitados = [item for item in matrizNodos if item not in nodosVisitados[0]]
        if np.random.rand() < probLim:
            arg = []
            for j in nodosNoVisitados:
                arg.append(feromona[nodosVisitados[0][-1]][j] * ((matrizDistancias[nodosVisitados[0][-1]][j]) ** valorHeur))
            arg = np.array(arg)
            max = np.where(arg == np.amax(arg))
            pobl[i][len(nodosVisitados[0])] = nodosNoVisitados[max[0][0]]
            feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0]) - 1]] = (
                    1 - factorEvapFerom) * feromona[pobl[i][len(nodosVisitados[0])]][
                pobl[i][len(nodosVisitados[0]) - 1]] + factorEvapFerom / (nodos * feromLocal)
            feromona[pobl[i][len(nodosVisitados[0]) - 1]][pobl[i][len(nodosVisitados[0])]] = feromona[
                pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0]) - 1]]
        else:
            arg = [0]
            for j in range(len(nodosNoVisitados)):
                arg.append(
                    feromona[nodosVisitados[0][-1]][nodosNoVisitados[j]] * ((matrizDistancias[nodosVisitados[0][-1]][nodosNoVisitados[j]]) ** valorHeur))
            arg = arg / np.sum(arg)
            arg = np.array(arg)
            arg = np.cumsum(arg)
            rand = np.random.rand()
            pos = np.where(arg < rand)
            pobl[i][len(nodosVisitados[0])] = nodosNoVisitados[pos[0][-1]]
            feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0]) - 1]] = (
                    1 - factorEvapFerom) * feromona[pobl[i][len(nodosVisitados[0])]][
                pobl[i][len(nodosVisitados[0]) - 1]] + factorEvapFerom / (nodos * feromLocal)
            feromona[pobl[i][len(nodosVisitados[0]) - 1]][pobl[i][len(nodosVisitados[0])]] = feromona[
                pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0]) - 1]]

    return pobl

# Comprobar que se proporcionan los argumentos esperados
if len(sys.argv) == 8:
    semilla = int(sys.argv[1])
    nombreArchivoOptTour = sys.argv[2]
    tamañoPob = int(sys.argv[3])
    numIt = int(sys.argv[4])
    factEvapFeromona = float(sys.argv[5])
    Heuristica = float(sys.argv[6])
    probLimite = float(sys.argv[7])
    print("Semilla: ", semilla)
    print("Archivo de Coordenadas: ", nombreArchivoOptTour)
    print("Tamaño de Población: ", tamañoPob)
    print("Número de Iteraciones: ", numIt)
    print("Factor de Evaporación de la Feromona: ", factEvapFeromona)
    print("Peso del Valor de la Heurística: ", Heuristica)
    print("Valor de Probabilidad Límite: ", probLimite)
else:
    print('Error en la entrada de los parámetros')
    sys.exit(0)

# Fijar la semilla aleatoria
np.random.seed(semilla)

# Leer las coordenadas de las ciudades desde el archivo
archivoCoordenadas = pd.read_csv(nombreArchivoOptTour, header=None, skiprows=6, skipfooter=1, engine='python', delim_whitespace=True, dtype=int)
matrizCoordenadas = archivoCoordenadas.to_numpy()
numVariables = matrizCoordenadas.shape[0]
matrizDistancias = obtenerDistancias(numVariables, matrizCoordenadas)
matrizHeuristicas = obtenerHeuristicas(matrizDistancias)

# Inicializar una solución inicial aleatoria y calcular su costo
mejorSolucion = np.arange(0, numVariables)
np.random.shuffle(mejorSolucion)
solucionMejorCosto = solucionCalcularCosto(numVariables, mejorSolucion, matrizDistancias)

# Inicializar la matriz de feromonas con valores iniciales
feromona = obtenerFeromonas(matrizDistancias, numVariables, solucionMejorCosto)
feromonaLocal = 1 / (solucionMejorCosto * numVariables)

# Inicio del ciclo principal de iteraciones
while numIt > 0 and not np.round(solucionMejorCosto, decimals=4) == 7544.3659:
    poblacion = inicializarHormigas(tamañoPob, numVariables)

    # Realizar la selección de segmentos para cada hormiga
    for i in range(tamañoPob):
        poblacion = seleccionarNuevoSegmento(numVariables, tamañoPob, poblacion, feromona, feromonaLocal, probLimite,
                                            matrizHeuristicas, Heuristica, factEvapFeromona)

    # Evaluar el costo de cada solución generada por las hormigas
    for i in range(tamañoPob):
        aux = solucionCalcularCosto(numVariables, poblacion[i][:], matrizDistancias)
        if aux < solucionMejorCosto:
            solucionMejorCosto = aux
            mejorSolucion = poblacion[i][:]
            print("En la iteración: ", numIt, " se encontró una mejor solución. Esta es: ", solucionMejorCosto)

    # Actualizar la feromona
    for i in range(numVariables):
        for j in range(numVariables):
            feromona[i][j] = (1 - factEvapFeromona) * feromona[i][j]
            feromona[j][i] = (1 - factEvapFeromona) * feromona[j][i]

    for i in range(len(mejorSolucion) - 1):
        feromona[mejorSolucion[i]][mejorSolucion[i + 1]] += factEvapFeromona / solucionMejorCosto
        feromona[mejorSolucion[i + 1]][mejorSolucion[i]] = feromona[mejorSolucion[i]][mejorSolucion[i + 1]]

    feromona[mejorSolucion[0]][mejorSolucion[-1]] = (1 - factEvapFeromona) * feromona[mejorSolucion[0]][mejorSolucion[-1]] + factEvapFeromona / solucionMejorCosto
    feromona[mejorSolucion[-1]][mejorSolucion[0]] = feromona[mejorSolucion[0]][mejorSolucion[-1]]
    # Información de la iteración

    print("Iteración: ", numIt)
    numIt -= 1

# Mostrar la mejor solución encontrada
print("Costo de la mejor solución: ", np.round(solucionMejorCosto, decimals=4), "\nSolución: ", mejorSolucion)
# Calcular el costo de la solución óptima desde el archivo berlin52.opt.tour
archivo_opt_tour = open("berlin52.opt.tour.txt", "r")
lineas = archivo_opt_tour.readlines()
archivo_opt_tour.close()
ciudades_opt_tour = [int(linea) for linea in lineas if linea.strip().isdigit()]
print("Longitud de ciudades_opt_tour:", len(ciudades_opt_tour))
print("Ciudades óptimas:", ciudades_opt_tour)

# Verificar que los índices en ciudades_opt_tour sean válidos y la longitud sea correcta
for idx in ciudades_opt_tour:
    if idx < 0 or idx >= numVariables:
        print("Error: índice de ciudad no válido en ciudades_opt_tour.")
        sys.exit(1)

if len(ciudades_opt_tour) != numVariables:
    print("Error: la longitud de ciudades_opt_tour no coincide con el número de ciudades.")
    sys.exit(1)

# Calcular el costo de la solución óptima
costo_solucion_optima = solucionCalcularCosto(len(ciudades_opt_tour), ciudades_opt_tour, matrizDistancias)

# Mostrar el costo de la solución generada
print("Costo de la solución generada por el algoritmo: ", np.round(solucionMejorCosto, decimals=4))

# Mostrar el costo de la solución óptima
print("Costo de la solución óptima: ", costo_solucion_optima)

# Compara los costos
if np.round(solucionMejorCosto, decimals=4) == costo_solucion_optima:
    print("La solución generada por el algoritmo es óptima.")
else:
    print("La solución generada por el algoritmo no es óptima.")
