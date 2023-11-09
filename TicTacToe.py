from Tablero import tablero
import random

# Definición de constantes
PUNTUACION_VICTORIA = 10
PUNTUACION_SITUACION_VENTAJOSA = 5
PUNTUACION_NEUTRAL = 0
PUNTUACION_SITUACION_PELIGROSA = -5
PUNTUACION_DERROTA = -10

def hay_ganador(tablero, jugador):
    for fila in range(3):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] == jugador:
            return True

    for columna in range(3):
        if tablero[0][columna] == tablero[1][columna] == tablero[2][columna] == jugador:
            return True

    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True

    return False

def hay_empate(tablero):
    for fila in tablero:
        if ' ' in fila:
            return False
    return True

def evaluar_tablero(tablero, jugador):
    if hay_ganador(tablero, jugador):
        return PUNTUACION_VICTORIA
    elif hay_ganador(tablero, 'O' if jugador == 'X' else 'X'):
        return PUNTUACION_DERROTA
    else:
        return PUNTUACION_NEUTRAL

def evaluar_futuro(tablero, jugador):
    if hay_ganador(tablero, jugador):
        return PUNTUACION_VICTORIA
    if hay_ganador(tablero, 'O' if jugador == 'X' else 'X'):
        return PUNTUACION_DERROTA

    mejor_puntuacion = PUNTUACION_SITUACION_PELIGROSA if jugador == 'X' else PUNTUACION_SITUACION_VENTAJOSA

    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == ' ':
                tablero[fila][columna] = jugador
                puntuacion = evaluar_futuro(tablero, 'O' if jugador == 'X' else 'X')
                tablero[fila][columna] = ' '

                if jugador == 'X':
                    mejor_puntuacion = max(mejor_puntuacion, puntuacion)
                else:
                    mejor_puntuacion = min(mejor_puntuacion, puntuacion)

    return mejor_puntuacion

def minimax(tablero, profundidad, jugador):
    if profundidad == 0 or hay_ganador(tablero, 'X') or hay_ganador(tablero, 'O'):
        return evaluar_tablero(tablero, 'O')

    if jugador == 'O':
        mejor_valor = float('-inf')
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == ' ':
                    tablero[fila][columna] = jugador
                    valor = minimax(tablero, profundidad - 1, 'X')
                    tablero[fila][columna] = ' '
                    mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == ' ':
                    tablero[fila][columna] = jugador
                    valor = minimax(tablero, profundidad - 1, 'O')
                    tablero[fila][columna] = ' '
                    mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def buscar_mejor_jugada(tablero, jugador):
    if jugador == 'X':
        mejor_valor = float('-inf')
        mejor_jugada = None

        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == ' ':
                    tablero[fila][columna] = jugador
                    valor = minimax(tablero, 9, 'O')
                    tablero[fila][columna] = ' '

                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_jugada = (fila + 1, columna + 1)
        return mejor_jugada
    else:
        jugadas_disponibles = [(fila + 1, columna + 1) for fila in range(3) for columna in range(3) if tablero[fila][columna] == ' ']
        return random.choice(jugadas_disponibles)

tablero_TicTac = tablero()

print("Tablero Vacío:")
for fila in tablero_TicTac:
    print(" | ".join(fila))
    print("-" * 9)

jugador = 'X'

while True:
    try:
        if jugador == 'X':
            mejor_jugada = buscar_mejor_jugada(tablero_TicTac, jugador)
            if mejor_jugada is not None:
                fila, columna = mejor_jugada
        else:
            fila = int(input("Introduce la fila (1-3): "))
            columna = int(input("Introduce la columna (1-3): "))

        if 1 <= fila <= 3 and 1 <= columna <= 3 and tablero_TicTac[fila - 1][columna - 1] == ' ':
            tablero_TicTac[fila - 1][columna - 1] = jugador
            print("Jugador " + jugador + " ha jugado.")
            for fila in tablero_TicTac:
                print(" | ".join(fila))
                print("-" * 9)

            if hay_ganador(tablero_TicTac, jugador):
                print("Jugador " + jugador + " ha ganado.")
                break
            elif hay_empate(tablero_TicTac):
                print("Empate.")
                break

            jugador = 'X' if jugador == 'O' else 'O'

        else:
            print("Introduce una jugada válida.")

    except ValueError:
        print("Por favor, introduce números para la fila y columna (1-3).")
