# Tarea 2 - Algoritmos Metaheurísticos Inspirados en la Naturaleza
Autores:

-Franco Avilés I. (faviles@ing.ucsc.cl)

-Hector Contreras M. (hcontreras@ing.ucsc.cl)

Desarrollar una aplicación que implemente el Problema del Vendedor Viajero a través del método de Sistema de Colonia de Hormigas

El código debe de tener al menos las siguientes funciones:

* Generar un número real randóminco entre [0 y 1).
* Generar un número entero randómico entre [0 y N].
* Inicializar una colonia de hormigas.
* Inicializar la feromona.
* Seleccionar el nuevo segmento de la ruta.
* Actualizar el nivel local de feromona.
* Actualizar el nivel global de feromona.
* Evaluar la ruta generada por una hormiga

Se deben ingresar y sintonizar los siguientes parámetros:
* Valor semilla generador valores randómicos.
* Archivo de entrada.
* Tamaño de la colonia o número de hormigas.
* Condición de término o número de iteraciones.
* Factor de evaporación de la feromona (α).
* El peso del valor de la heurística (β).
* Valor de probabilidad límite (q0).

## Instalación
Requisitos: Python 3.8.10 disponible en sistema operativo.

## Ejecución
Para ejecutar, escribir en consola o terminal:
```ruby
py ColoniaHormigas.py <Semilla> <Archivo> <Tamaño_Pob> <Iteraciones> <Factor_Evap> <Valor_Heur> <Prob_Limite>
```
donde:
* Semilla: Valor entero positivo que representa la semilla.
* Archivo: Archivo de entrada con  coordenadas de los nodos de la matriz.
* Tamaño_Pob: Valor entero que represneta el tamaño de la colonia o número de hormigas.
* Iteraciones: Valor entero que rige número de iteraciones (condición de término).
* Factor_Evap: Valor entero entre 0 y 1 que representa factor de evaporación de la feromona.
* Valor_Heur: Valor entero entre 0 y 1 que representa el peso del valor de la heurística.
* Prob_Limite: Valor entero entre 0 y 1 de probabilidad límite.
  
## Ejemplo
```ruby
py ColoniaHormigas.py 1 berlin52.opt.tour 50 100 0.2 2.5 0.8
```
