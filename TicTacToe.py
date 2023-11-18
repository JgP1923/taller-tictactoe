from copy import deepcopy
from Tablero import tablero

# Definición de constantes
PUNTUACION_VICTORIA = 10
PUNTUACION_SITUACION_VENTAJOSA = 5
PUNTUACION_NEUTRAL = 0
PUNTUACION_SITUACION_PELIGROSA = -5
PUNTUACION_DERROTA = -10

def hay_ganador(tablero, jugador):
    # Verificar filas y columnas
    for i in range(3):
        if all(tablero[i][j] == jugador for j in range(3)) or all(tablero[j][i] == jugador for j in range(3)):
            return True

    # Verificar diagonales
    if all(tablero[i][i] == jugador for i in range(3)) or all(tablero[i][2 - i] == jugador for i in range(3)):
        return True

    return False


def hay_empate(tablero):
    for fila in tablero:
        if ' ' in fila:
            return False
    return True

def evaluar_futuro(tablero, jugador, perspectiva):
    if hay_empate(tablero):
        return PUNTUACION_NEUTRAL
    if hay_ganador(tablero, jugador):
        return PUNTUACION_VICTORIA if jugador == perspectiva else PUNTUACION_DERROTA
    else:
        mejor_puntuacion = (
            PUNTUACION_SITUACION_PELIGROSA
            if jugador == perspectiva
            else PUNTUACION_SITUACION_VENTAJOSA
        )
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == ' ':
                    tablero[fila][columna] = jugador
                    puntuacion = evaluar_futuro(deepcopy(tablero), 'O' if jugador == 'X' else 'X', perspectiva)
                    tablero[fila][columna] = ' '

                    if jugador == perspectiva:
                        mejor_puntuacion = max(mejor_puntuacion, puntuacion)
                    else:
                        mejor_puntuacion = min(mejor_puntuacion, puntuacion)

    return mejor_puntuacion




def imprimir_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)

def imprimir_jugadas_siguientes(tablero, jugador):
    print("\nPosibles Jugadas en el Siguiente Movimiento:")
    
    for i in range(1, 10):
        fila = (i - 1) // 3
        columna = (i - 1) % 3

        if tablero[fila][columna] == ' ':
            tablero[fila][columna] = jugador
            puntuacion = evaluar_futuro(deepcopy(tablero), 'O' if jugador == 'X' else 'X', jugador)
            tablero[fila][columna] = ' '

            if puntuacion == PUNTUACION_VICTORIA:
                print(f"Jugada: ({fila + 1}, {columna + 1}), Puntuación: 10 (Victoria)")
            elif puntuacion >= PUNTUACION_SITUACION_VENTAJOSA:
                print(f"Jugada: ({fila + 1}, {columna + 1}), Puntuación: 5 (Ventajosa)")
            elif puntuacion == PUNTUACION_NEUTRAL:
                print(f"Jugada: ({fila + 1}, {columna + 1}), Puntuación: 0 (Neutral)")
            elif puntuacion <= PUNTUACION_SITUACION_PELIGROSA:
                print(f"Jugada: ({fila + 1}, {columna + 1}), Puntuación: -5 (Peligrosa)")
            elif puntuacion == PUNTUACION_DERROTA:
                print(f"Jugada: ({fila + 1}, {columna + 1}), Puntuación: -10 (Derrota)")

tablero_TicTac = tablero()

print("Tablero Inicial:")
imprimir_tablero(tablero_TicTac)

jugador = 'X'

while True:
    try:
        imprimir_jugadas_siguientes(tablero_TicTac, jugador)
        fila = int(input("Introduce la fila (1-3): "))
        columna = int(input("Introduce la columna (1-3): "))

        if 1 <= fila <= 3 and 1 <= columna <= 3 and tablero_TicTac[fila - 1][columna - 1] == ' ':
            tablero_TicTac[fila - 1][columna - 1] = jugador
            print(f"Jugador {jugador} ha jugado:")
            imprimir_tablero(tablero_TicTac)

            if hay_ganador(tablero_TicTac, jugador):
                print(f"Jugador {jugador} ha ganado.")
                break
            elif hay_empate(tablero_TicTac):
                print("Empate.")
                break

            jugador = 'X' if jugador == 'O' else 'O'

        else:
            print("Introduce una jugada válida.")

    except ValueError:
        print("Por favor, introduce números para la fila y columna (1-3).")
