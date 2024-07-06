import random

'''
Esta clase representa una celula primitiva
'''
class Cell:
    # Definir un color predeterminado para la celula muerta
    __BLACK = (0,0,0)
    # Definir si dicha celula hace parte de un organismo
    __isOrganism = None

    '''
    Metodo constructor para el objeto
    :param prob: define la probabilidad de simbiosis de la celula
    :param color: define el color de dicha celula
    '''
    def __init__(self, prob: float = random.random(), color: tuple[int, int, int] = __BLACK):
        if 0 < prob < 1:
            self.__prob_symb = prob
        else:
            self.__prob_symb = random.random()
        self.__color = color

    '''
    Metodo getter del estado de la celula
    :return: (True) si hace parte de un organismo o (False) si no
    '''
    @property
    def isOrganism(self):
        return self.__isOrganism

    '''
    Metodo getter del color de la celula
    :retrun: color de la celula
    '''
    @property
    def color(self):
        return self.__color

    '''
    Metodo getter del valor de la probabilidad de simbiosis entre celulas
    :return: probabilidad de simbiosis
    '''
    @property
    def prob_symb(self) -> float:
        return self.__prob_symb