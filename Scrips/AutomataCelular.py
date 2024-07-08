import random
import pygame
import numpy as np

'''
Esta clase representa el automata celular
'''
class AC:
    # Definir el numero de las celdas del automata celular
    __nX = 95
    __nY = 93

    # Definir los posibles de las celulas y su probabilidad de nacimiento (rojo, verde y azul)
    __COLORS = {(255, 0, 0): 0.4, (0, 255, 0): 0.4, (0, 0, 255): 0.2}

    # Definir las poblaciones iniciales del automata
    __MIN = 500
    __MAX = 1500

    # Difinir las reglas del juego de todas las celulas
    # (n > 0) se atraen, (n < 0) se repelen y (n = 0) son neutros
    __Fmax = ((0.05, -0.8, 1.47), # Rojo
              (0.47, 0.07, -1.66), # Verde
              (-1.74, 0.14, 0.05)) # Azul
    # Definir la longitud maxima en el que se aplica la fuerza
    __Rmax = (5, 5, 5)
    # Definir la longitud minima en el que se aplica la fuerza inversa
    __Rmin = (2, 2, 2)
    # Definir las contantes universales
    __Ke = 9
    __N = -0.4
    __FRICTION_FACTOR = 1
    __FRICTION_RATE = 0.01

    '''
    Metodo constructor del automata celular
    '''
    def __init__(self):
        # Definir las iteraciones del automata celular
        self.__iterations = 0
        self.__cells = np.zeros((self.__nY, self.__nX), dtype=tuple)
        self.__aux = np.zeros((self.__nY, self.__nX), dtype=tuple)

        # Crear aleatoriamente los colores en las celdas
        poblation_initial = random.randint(self.__MIN, self.__MAX)
        colors = list(self.__COLORS.keys())
        prob = list(self.__COLORS.values())
        visit = set()

        # Poblar el automata
        for _ in range(poblation_initial):
            # Evitar que se repitan algunas celdas ya pintadas
            while True:
                x = random.randint(0, self.__nX-1)
                y = random.randint(0, self.__nY-1)
                # Se pinta la celda:
                if (x, y) not in visit:
                    visit.add((x, y))
                    current_color = random.choices(colors, prob)[0]
                    self.__cells[y][x] = current_color
                    break

    '''
    Metodo para devolver el valor de una celda dadas sus coordenadas en el espacio reflectante
    :param x: coordenada x del espacio
    :param y: coordenada y del espacio
    :return: valor de la celda
    '''
    def read(self, y: int, x: int) -> tuple[int, int, int]:
        # Aplicar reflexión en las coordenadas x e y
        x %= self.__nX
        y %= self.__nY

        return self.__cells[y, x]

    '''
    Metodo para devolver una seccion de celdas dadas sus coordenadas en el espacio y su tamaño
    :param x_init: coordenada inicial x del espacio
    :param y_init: coordenada inicial y del espacio
    :param x_final: coordenada final x del espacio
    :param y_final: coordenada final y del espacio
    '''
    def read_all(self, y: int, x: int, dist: int) -> np.ndarray:
        rows_neighborn = (y + np.arange(-dist, dist + 1)) % self.__nY
        cols_neighborn = (x + np.arange(-dist, dist + 1)) % self.__nX
        # Generar todas las combinaciones posibles de las coordenadas de los vecinos
        idx_rows, idx_cols = np.ix_(rows_neighborn, cols_neighborn)

        # Obtener todas las celdas que componen a esa seccion
        neighborns = self.__cells[idx_rows, idx_cols]

        return neighborns

    '''
    Metodo para obtener las celulas vivas del automata
    :return: un diccionario con el numero de celulas de cada tipo
    '''
    def lives(self) -> dict:
        colors = list(self.__COLORS)
        liveCells = {color: 0 for color in colors}
        for y in range(self.__nY):
            for x in range(self.__nX):
                current = self.read(y, x)
                if current != 0:
                    liveCells[current] += 1
        return liveCells

    '''
    Metodo para actualizar el estado del automata celular ejecutando una iteracion
    '''
    def update(self):
        self.__iterations += 1
        if self.__FRICTION_FACTOR > 0.005:
            self.__FRICTION_FACTOR -= self.__FRICTION_RATE
        colors = list(self.__COLORS.keys())
        prob = list(self.__COLORS.values())
        # Crear la pila para aquellas celulas que no encuentren destino
        stack = []
        for y in range(self.__nY):
            for x in range(self.__nX):
                current = self.read(y, x)
                # Si la celda está apagada
                if current == 0:
                    current_aux = self.__aux[y, x]
                    if current_aux == 0:  # Si la celda actual en el automata auxiliar está desocupada
                        neighbors = self.read_all(y, x, 1)[0].flatten()
                        neighbors_count = np.sum(neighbors != 0)
                        if neighbors_count == 3:
                            # Elegir un color aleatorio para la nueva célula
                            new_color = random.choices(colors, prob)[0]
                            if random.random() < self.__COLORS[new_color]:
                                self.__aux[y, x] = new_color
                    continue

                current_index = colors.index(current)
                r_min_current = self.__Rmin[current_index]
                r_max_current = self.__Rmax[current_index]

                # vector fuerza, cada posicion es la distancia (x, y) de desplazamiento
                v_fuerza = [0, 0]

                # obtener por todas las celulas vecinas que le afectan
                near = self.read_all(y, x, r_max_current)

                # Recorrer la matriz de celdas vecinas
                for i, _ in enumerate(near):
                    for j, neighbor_color in enumerate(_):
                        # Evitar pasar por la misma celda actual
                        if (j == r_max_current and i == r_max_current) or neighbor_color == 0:
                            continue

                        # Obtener las distancias de la celda vecina hasta la celda actual
                        r_y = i - r_max_current
                        r_x = r_max_current - j

                        # Verificar que tan cerca esta celda vecina a la actual
                        const = self.__N if ((-r_min_current <= r_x <= r_max_current) and
                                             -r_min_current <= r_y <= r_min_current) else 1

                        neighbor_index = colors.index(neighbor_color)
                        # Almacenar las cargas de las celdas segun su distancia y color
                        q1 = const * self.__Fmax[neighbor_index][current_index]
                        q2 = const * self.__Fmax[current_index][neighbor_index]

                        # Operar la ecuacion de Coulomb
                        v_ = self.coulomb(q1, q2, r_y, r_x)
                        v_fuerza[0] += v_[0]
                        v_fuerza[1] += v_[1]

                # Obtener la proxima celda y actual en el automata auxiliar.
                pos_x = int(x + np.round(v_fuerza[0])) % self.__nX
                pos_y = int(y + np.round(v_fuerza[1])) % self.__nY
                next_aux = self.__aux[pos_y, pos_x]
                current_aux = self.__aux[y, x]

                # Mover la celda
                if next_aux == 0: # Si la celda siguiente está desocupada
                    self.__aux[pos_y, pos_x] = current
                elif current_aux == 0: # Si la celda actual está desocupada
                    self.__aux[y, x] = current
                else: # Si ambas celdas están ocupadas
                    stack.append((y, x, pos_y, pos_x, current))

        # Buscar un lugar cercano a cada una de las celulas en espera
        for orig_y, orig_x, new_y, new_x, cell in stack:
            neighbors = self.read_all(new_y, new_x, 1)[0].flatten()
            neighbors_count = np.sum(neighbors != 0)
            # La celula sobrevive si se cumplen las reglas del juego de la vida, en otro caso no
            if neighbors_count == 3 or neighbors_count == 2:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        ny, nx = (new_y + dy) % self.__nY, (new_y + dx) % self.__nX
                        if self.__aux[ny, nx] == 0:
                            self.__aux[ny, nx] = cell
                            break

        # Actualizar el automata principal
        self.__cells = self.__aux
        self.__aux = np.zeros((self.__nY, self.__nX), dtype=tuple)

    '''
    Metodo que realiza el calculo de la ley de coulomb
    :param q1: carga de la particula 1
    :param q2: carga de la particula 2
    :param r_x: vector x coordenada
    :param r_y: vector y coordenada
    :return: vector de fuerza electrica de las particulas
    '''
    def coulomb(self, q1, q2, r_y, r_x) -> np.array:
        norm_2 = r_x**2 + r_y**2
        v_fuerza = ((self.__Ke * ((q1 * q2) / norm_2)) * (r_x/(norm_2**0.5)),
                    (self.__Ke * ((q1 * q2) / norm_2)) * (r_y/(norm_2**0.5)))
        # Aplicar el factor de fricción a la fuerza calculada
        v_fuerza = (v_fuerza[0]*self.__FRICTION_FACTOR, v_fuerza[1] * self.__FRICTION_FACTOR)
        return v_fuerza

    '''
    Metodo de proyeccion del espacio con las celdas del automata celular
    :param context: representa el contexto gráfico de la ventana
    '''
    def draw(self, context : pygame.Surface):
        for y in range(self.__nY):
            for x in range(self.__nX):
                current = self.read(y, x)
                if current != 0:
                    # Dibujar un rectangulo relleno del color de la celula
                    pygame.draw.rect(context, current, (x * 10, y * 10, 10, 10))
                # Dibujar un recuadro sin relleno con bordes grises
                else:
                    pygame.draw.lines(context, (64, 64, 64), True, (
                        (x * 10, y * 10),
                        ((x + 1) * 10, y * 10),
                        ((x + 1) * 10, (y + 1) * 10),
                        (x * 10, (y + 1) * 10)
                    ), 1)

    '''
    Metodo getter de las iteraciones actuales del automata celular
    :return: numero de iteraciones
    '''
    @property
    def iterations(self) -> int:
        return self.__iterations