import random
import Cell

'''
Esta clase representa un organismo pluricelular, es una lista de celulas
'''
class Symbionts:
    __cells = [] # variable que contiene las celulas que componen el organismo

    '''
    Metodo constructor para el objeto
    :param cells: lista de celulas
    :param prob: probabilidad de simbiosis del organismo
    '''
    def __init__(self, cells, prob: float = random.random()):
        self.add_organism(cells)
        size = len(cells) # tamaño del vector de celulas
        self.__hunger = random.randint(0, 3+size) # hambre actual del organismo
        if 0 < prob < 1:
            self.__prob_symb= prob
        else:
            self.__prob_symb = random.random()
        self.__age = 0
        self.__max_age = random.randint(60//size, 250//size)

    '''
    Metodo getter de la variable de probabilidad de simbiosis
    :return: probabilidad de simbiosis
    '''
    @property
    def prob_symb(self) -> float:
        return self.__prob_symb

    '''
    Metodo getter del listado de celulas que componen el organismo
    :return: lista de celulas que componen el organismo
    '''
    @property
    def cells(self) -> list:
        return self.__cells

    '''
    Metodo para agregar nuevas celulas al organismo
    :param cells: lista de celulas nuevas a agregar
    '''
    def add_organism(self, cells: set[Cell]):
        if len(cells) > 1:
            self.__cells.extend(cells)

    '''
    Metodo getter de la edad actual del organismo
    :return: edad actual
    '''
    @property
    def age(self) -> int:
        return self.__age

    '''
    Metodo getter de la edad de muerte del organismo
    :return: edad de fallecimiento
    '''
    @property
    def max_age(self) -> int:
        return self.__max_age

    '''
    Metodo setter para actualizar la edad del organismo en años
    '''
    def birthday(self):
        self.__age += 1

    '''
    Metodo setter para actualizar el valor del hambre del organismo, simular que ha comido
    :param hunger: valor de la comida ingerida por el organismo
    '''
    def eat(self, hunger: int):
        if hunger > self.__hunger:
            hunger = self.__hunger
        self.__hunger -= hunger

    '''
    Metodo setter para actualizar el valor del hambre del organismo
    '''
    def give_hunger(self):
        self.__hunger += 1