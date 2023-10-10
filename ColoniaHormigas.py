import sys
import pandas as pd
import numpy as np

def obtenerDistancias(numVar,matriz):
    matrizDistancias = np.full((numVar,numVar), fill_value=-1.0, dtype=float)

    for i in range(numVar-1):
        for j in range(i+1, numVar):
            distancia = np.sqrt(np.sum(np.square(matriz[i]-matriz[j])))
            matrizDistancias[i][j] = distancia
            matrizDistancias[j][i] = distancia

    return matrizDistancias

def obtenerHeuristicas(matriz):
    matrizHeuristicas = np.full_like(matriz, fill_value=(1/matriz), dtype=float)
    np.fill_diagonal(matrizHeuristicas, 0.0)

    return matrizHeuristicas

def obtenerFeromonas(matriz,numVar,mejorCosto):
    matrizFeromonas = np.full_like(matriz, 1/(mejorCosto*numVar))

    return matrizFeromonas

def solucionCalcularCosto(cantNodos,matrizSolucion,matrizBase):
    costo = matrizBase[matrizSolucion[cantNodos-1]][matrizSolucion[0]]
    for i in range(cantNodos-1):
        costo = costo + (matrizBase[matrizSolucion[i]][matrizSolucion[i+1]])

    return costo

def inicializarHormigas(hormiga, nodos):
    poblacion = np.full((hormiga, nodos), -1)
    for i in range(hormiga):
        poblacion[i][0] = float(np.random.randint(nodos))

    return poblacion

def seleccionarNuevoSegmento(nodos,tamañoPobl,pobl,feromona,feromLocal,probLim,matrizDistancias,valorHeur,factorEvapFerom):
    matrizNodos = np.arange(nodos)
    for i in range(tamañoPobl):
        row = pobl[i][:]
        nodosVisitados = np.where(row != -1)
        nodosVisitados = [pobl[i][item] for item in nodosVisitados]
        nodosNoVisitados = [item for item in matrizNodos if item not in nodosVisitados[0]]
        if np.random.rand() < probLim:
            arg = []
            for j in nodosNoVisitados:
                arg.append(feromona[nodosVisitados[0][-1]][j]*((matrizDistancias[nodosVisitados[0][-1]][j])**valorHeur))
            arg = np.array(arg)
            max = np.where(arg == np.amax(arg))
            pobl[i][len(nodosVisitados[0])] = nodosNoVisitados[max[0][0]]
            feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0])-1]] = (1-factorEvapFerom)*feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0])-1]] + factorEvapFerom/(nodos*feromLocal)
            feromona[pobl[i][len(nodosVisitados[0])-1]][pobl[i][len(nodosVisitados[0])]] = feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0])-1]]
        else:
            arg = [0]
            for j in range(len(nodosNoVisitados)):
                arg.append(feromona[nodosVisitados[0][-1]][nodosNoVisitados[j]]*((matrizDistancias[nodosVisitados[0][-1]][nodosNoVisitados[j]])**valorHeur))
            arg = arg/np.sum(arg)
            arg = np.array(arg)
            arg = np.cumsum(arg)
            rand = np.random.rand()
            pos = np.where(arg < rand)
            pobl[i][len(nodosVisitados[0])] = nodosNoVisitados[pos[0][-1]]
            feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0])-1]] = (1-factorEvapFerom)*feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0])-1]] + factorEvapFerom/(nodos*feromLocal)
            feromona[pobl[i][len(nodosVisitados[0])-1]][pobl[i][len(nodosVisitados[0])]] = feromona[pobl[i][len(nodosVisitados[0])]][pobl[i][len(nodosVisitados[0])-1]]
            
    return pobl

if len(sys.argv) == 8:
    semilla = int(sys.argv[1])
    matrizCoordenadas = str(sys.argv[2])
    tamañoPob = int(sys.argv[3])
    numIt = int(sys.argv[4])
    factEvapFeromona = float(sys.argv[5])
    Heuristica = float(sys.argv[6])
    probLimite = float(sys.argv[7])
    print("Semilla: ", semilla)
    print("Matriz de Coordenadas: ", matrizCoordenadas)
    print("Tamaño de Población: ", tamañoPob)
    print("Número de Iteraciones: ", numIt)
    print("Factor de Evaporación de la Feromona: ", factEvapFeromona)
    print("Peso del Valor de la Heuristica: ", Heuristica)
    print("Valor de Probabilidad Límite: ", probLimite)
else:
    print('Error en la entrada de los parametros')
    sys.exit(0)

np.random.seed(semilla)

archivo = pd.read_csv("burma14.txt", header=None, skiprows=6, skipfooter=1, engine='python', delim_whitespace=True, usecols=(1,2), dtype=int)
matrizArchivo  = archivo.to_numpy()
numVariables = matrizArchivo.shape[0]
matrizDistancias = obtenerDistancias(numVariables,matrizArchivo)
matrizHeuristicas = obtenerHeuristicas(matrizDistancias)
mejorSol = np.arange(0,numVariables)
np.random.shuffle(mejorSol)
solucionMejorCosto = solucionCalcularCosto(numVariables,mejorSol,matrizDistancias)
feromona = obtenerFeromonas(matrizDistancias,numVariables,solucionMejorCosto)
feromonaLocal = 1/(solucionMejorCosto*numVariables)

while numIt > 0 and not np.round(solucionMejorCosto,decimals=4) == 7544.3659:
    poblacion = inicializarHormigas(tamañoPob, numVariables)

    for i in range(numVariables-1):
        poblacion = seleccionarNuevoSegmento(numVariables,tamañoPob,poblacion,feromona,feromonaLocal,probLimite,matrizHeuristicas,Heuristica,factEvapFeromona)

    for i in range(tamañoPob):
        aux = solucionCalcularCosto(numVariables,poblacion[i][:],matrizDistancias)
        if aux < solucionMejorCosto:
            solucionMejorCosto = aux
            mejorSolucion = poblacion[i][:]
            print("En la iteración: ", numIt, " se encontró una mejor solución. Esta es: ", solucionMejorCosto)

    for i in range(numVariables):
        for j in range(numVariables):
            feromona[i][j] = (1-factEvapFeromona)*feromona[i][j]
            feromona[j][i] = (1-factEvapFeromona)*feromona[j][i]
    
    for i in range(len(mejorSolucion)-1):
        feromona[mejorSolucion[i]][mejorSolucion[i + 1]] += factEvapFeromona/solucionMejorCosto
        feromona[mejorSolucion[i + 1]][mejorSolucion[i]] = feromona[mejorSolucion[i]][mejorSolucion[i + 1]]
    
    feromona[mejorSolucion[0]][mejorSolucion[-1]] = (1-factEvapFeromona)*feromona[mejorSolucion[0]][mejorSolucion[-1]] + factEvapFeromona/solucionMejorCosto
    feromona[mejorSolucion[-1]][mejorSolucion[0]] = feromona[mejorSolucion[0]][mejorSolucion[-1]]

    print("Iteración: ",numIt)
    numIt -= 1

print("Costo mejor solución: ", np.round(solucionMejorCosto,decimals=4), "\nSolución: ", mejorSolucion)
