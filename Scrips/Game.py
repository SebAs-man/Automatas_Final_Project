import pygame
import sys
from AutomataCelular import AC

# Definir el tamaño de la ventana
__SCREEN_WIDTH = 950
__SCREEN_HEIGHT = 1000
__size = (__SCREEN_WIDTH, __SCREEN_HEIGHT)

# Definir los colores de las celulas
__WHITE = (255, 255, 255)
__BLUE = (0, 0, 255)
__GREEN = (0, 255, 0)
__RED = (255, 0, 0)
__BLACK = (0, 0, 0)

def main():
    # Instancias de la ventana
    pygame.init()
    pygame.font.init()
    # Creacion del automata celular
    world = AC()
    # Creacion de la ventana principal
    screen = pygame.display.set_mode(__size)
    pygame.display.set_caption('Juego de la vida aumentado')

    # Crear el reloj del juego
    clock = pygame.time.Clock()

    # Estado inicial del juego
    start = False

    # Carga las imagenes PNG para los botones de control
    save = pygame.image.load('Images/save.png')
    save_rect = save.get_rect()
    save_rect = save_rect.move(225, 934)
    load = pygame.image.load('Images/load.png')
    load_rect = load.get_rect()
    load_rect = load_rect.move(300, 934)
    play = pygame.image.load('Images/play.png')
    play_rect = play.get_rect()
    play_rect = play_rect.move(10, 934)
    pause = pygame.image.load('Images/pause.png')
    pause_rect = pause.get_rect()
    pause_rect = pause_rect.move(125, 934)

    # Carga el sonido
    sound_pause = pygame.mixer.Sound('Sounds/pause.mp3')
    sound_start = pygame.mixer.Sound('Sounds/start.mp3')

    # Define la funte del texto a mostrar
    font = pygame.font.Font('Fonts/PressStart2P.ttf', 12)
    # Carga los textos para mostrar informacion del juego
    text_play = font.render("Press start", True, (255, 255, 255))
    text_play_rect = text_play.get_rect()
    text_play_rect = text_play_rect.move(120, 959)
    text_iteration = font.render('Iterations', True, (255, 255, 255))
    text_iteration_rect = text_iteration.get_rect()
    text_iteration_rect = text_iteration_rect.move(335, 947)
    text_cell1 = font.render('Poblation', True, (255, 0, 0))
    text_cell1_rect = text_cell1.get_rect()
    text_cell1_rect = text_cell1_rect.move(485,947)
    text_cell2 = font.render('Poblation', True, (0, 255, 0))
    text_cell2_rect = text_cell2.get_rect()
    text_cell2_rect = text_cell2_rect.move(635, 947)
    text_cell3 = font.render('Poblation', True, (61, 200, 254))
    text_cell3_rect = text_cell3.get_rect()
    text_cell3_rect = text_cell3_rect.move(785, 947)
    text_pause = font.render('Pause', True, (255, 255, 255))
    text_pause_rect = text_pause.get_rect()
    text_pause_rect = text_pause_rect.move(50, 961)

    # Estado del automata celular
    running = True

    while True:
        # se capturan los eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('End.')
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start:
                    running = not running
                    sound_pause.play()
                else:
                    if not start:
                        sound_start.play()
                    start = True
                    load_rect = load_rect.move(1100, 1100)
                    play_rect = play_rect.move(1000, 1100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if pos_mouse[1] > 930:
                    if save_rect.collidepoint(pos_mouse) and start:
                        print('se ha guardado')
                    if load_rect.collidepoint(pos_mouse):
                        print('se ha cargado')
                    if play_rect.collidepoint(pos_mouse):
                        start = True
                        sound_start.play()
                        load_rect = load_rect.move(1000, 1100)
                        play_rect = play_rect.move(1000,1100)
                    if pause_rect.collidepoint(pos_mouse):
                        running = not running
                        sound_pause.play()

        # Pintar la pantalla para darle mas estilo
        screen.fill((25, 25, 25))
        pygame.draw.line(screen, __WHITE, (0, 931), (950,931), 2)
        pygame.draw.line(screen, __WHITE, (295, 931), (295, 1000),2)

        # Añadir a la pantalla las imágenes para representar los botones
        screen.blit(load, load_rect)
        screen.blit(play, play_rect)
        if start:
            screen.blit(save, save_rect)
            world.draw(screen)
            liveCells = world.lives()
            if running:
                world.update()
            else:
                screen.blit(pause, pause_rect)
                screen.blit(text_pause, text_pause_rect)
            # Añadir a la pantalla los textos informativos
            screen.blit(text_iteration, text_iteration_rect)
            screen.blit(text_cell1, text_cell1_rect)
            screen.blit(text_cell2, text_cell2_rect)
            screen.blit(text_cell3, text_cell3_rect)
            # Anañadir a la pantalla las estadísticas del juego
            screen.blit(font.render(str(world.iterations), True, (255, 255, 255)),(371,971))
            screen.blit(font.render(str(liveCells[__RED]), True, (255, 0, 0)), (521, 971))
            screen.blit(font.render(str(liveCells[__GREEN]), True, (0, 255, 0)), (671, 971))
            screen.blit(font.render(str(liveCells[__BLUE]), True, (61, 200, 254)), (821, 971))
        else:
            screen.blit(text_play, text_play_rect)

        # Refresco de la ventana
        pygame.display.flip()
        clock.tick(60)

'''
Ejecucion del juego de la vida aumentada
'''
if __name__ == "__main__":
    main()



