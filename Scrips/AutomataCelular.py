import random
import pygame
from Cell import Cell

'''
Esta clase representa el automata celular
'''
class AC:
    # Definir el numero de las celdas del automata celular
    __nX = 95
    __nY = 93
    # Definir el vector de celdas y su respectivo respaldo
    __cells = []
    __next = []

    # Definir los colores de las celulas
    __BLUE = (0, 0, 255)
    __GREEN = (0, 255, 0)
    __RED = (255, 0, 0)

    # Definir las probabilidades de simbiosis
    __probB = 0.33333
    __probG = 0.33333
    __probR = 0.33333

    # Definir las iteraciones del automata celular
    __iterations = 0

    '''
    Metodo constructor del automata celular
    '''
    def __init__(self):
        # Crear las celdas del automata celular
        for row in range(self.__nY):
            row = []
            for col in range(self.__nX):
                row.append(self.Celda())
            self.__cells.append(row)
        # Crear aleatoriamente celulas en las celdas
        pos_cells = set()
        poblation_initial = random.randint(5000, 7000)
        div = poblation_initial // 3
        for i in range(poblation_initial):
            while True:
                x = random.randint(0, self.__nX-1)
                y = random.randint(0, self.__nY-1)
                if (x, y) not in pos_cells:
                    pos_cells.add((x, y))
                    if i < div:
                        self.__cells[y][x].celula = Cell(self.__probR, self.__RED)
                    elif div <= i < 2*div:
                        self.__cells[y][x].celula = Cell(self.__probG, self.__GREEN)
                    else:
                        self.__cells[y][x].celula = Cell(self.__probB, self.__BLUE)
                    break

    '''
    Metodo para devolver el valor de una celda dadas sus coordenadas en el espacio reflectante
    :param x: coordenada x del espacio
    :param y: coordenada y del espacio
    :return: valor de la celda
    '''
    def read(self, x: int, y: int):
        # verificar si se refleja en las coordenadas x
        if x >= self.__nX:
            x -= self.__nX
        elif x < 0:
            x += self.__nX
        # verificar si se refleja en las coordenadas y
        if y >= self.__nY:
            y -= self.__nY
        elif y < 0:
            y += self.__nY

        return self.__cells[y][x]

    '''
    Metodo para obtener las celulas vivas del automata
    :return: un diccionario con el numero de celulas de cada tipo
    '''
    def lives(self) -> dict:
        liveCells = {self.__GREEN: 0, self.__BLUE: 0, self.__RED: 0}
        for y in range(self.__nY):
            for x in range(self.__nX):
                current = self.read(x, y)
                if current.enabled:
                    color = current.celula.color
                    liveCells[color] += 1
        return liveCells

    '''
    Metodo para actualizar el estado del automata celular ejecutando una iteracion
    '''
    def update(self):
        self.__iterations += 1
        for y in range(self.__nY):
            next_row = []
            for x in range(self.__nX):
                # Celdas vecinas
                near = [
                    self.read(x-1, y+1),
                    self.read(x, y+1),
                    self.read(x+1, y+1),
                    self.read(x-1, y),
                    self.read(x+1, y),
                    self.read(x-1, y-1),
                    self.read(x, y-1),
                    self.read(x+1, y-1)
                ]
                # Contar las celulas vecinas vivas
                colors = {self.__GREEN: 0, self.__RED: 0, self.__BLUE: 0}
                for neighbor in near:
                    if neighbor.enabled:
                        color_neighbor = neighbor.celula.color
                        colors[color_neighbor] += 1

                current = self.read(x, y)
                # Muere una celula
                if current.enabled:
                    current_color = current.celula.color
                    count_other = 0
                    for color, count in colors.items():
                        if color != current_color:
                            count_other += count
                    if colors[current_color] != 2 and colors[current_color] != 3:
                        current = self.Celda()
                # Nace una celula
                else:
                    prob = [self.__probG, self.__probR, self.__probB]
                    count_max = 0
                    key_max = None
                    pos_max = -1
                    for i, (color, count) in enumerate(colors.items()):
                        if count * prob[i] >= count_max:
                            pos_max = i
                            count_max = count * prob[i]
                            key_max = color
                    if sum(colors.values()) == 3:
                        current = self.Celda()
                        current.celula = Cell(prob[pos_max], key_max)

                # Guardar los cambios en el automata de respaldo
                next_row.append(current)
            self.__next.append(next_row)
        # Agregar los cambios realizados al automata principal
        self.__cells = self.__next
        self.__next = []

    '''
    Metodo de proyeccion del espacio con las celdas del automata celular
    :param context: representa el contexto gráfico de la ventana
    '''
    def draw(self, context:pygame.Surface):
        for y in range(self.__nY):
            for x in range(self.__nX):
                current = self.read(x, y)
                # Verificar si la celda esta activada
                if current.enabled:
                    color = current.celula.color
                    # Dibujar un rectangulo relleno del color de la celula
                    pygame.draw.rect(context, color, (x * 10, y * 10, 10, 10))
                else:
                    # Dibujar un recuadro sin relleno con bordes grises
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

    '''
    Esta clase interna representa una celda del automata celular
    '''
    class Celda:
        '''
        Metodo constructor de una celda que se encuentra en el automata celular
        '''
        def __init__(self):
            self.__celula = None

        '''
        Metodo getter de la celula que se encuentra encima de la celda
        :return: (None) si no hay nada o la celula ubicada en la celda
        '''
        @property
        def celula(self):
            return self.__celula

        '''
        Metodo getter del estado actual de la celda
        :return: (True) si esta activada o (False) si no
        '''
        @property
        def enabled(self) -> bool:
            return self.__celula is not None

        '''
        Metodo setter para cambiar la celula que se encuentra sobre dicha celda
        :param cell: define la celula que se pondra sobre la celda
        '''
        @celula.setter
        def celula(self, cell: Cell):
            self.__celula = cell