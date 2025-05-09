from menu import *

pygame.mixer.init(frequency=44100, size=-16, channels=2)

pygame.init()

pygame.mixer.music.load("sound/startup.wav")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=-1)

if __name__ == '__main__':
    pygame.display.set_caption('Tic-Tac-Toe')
    icon = pygame.image.load('img/icon.png')
    pygame.display.set_icon(icon)
    menu = MenuIntro()
    menuSizeHuman = MenuSizeHuman()
    menuAI = MenuAI()
    menuAlgo = MenuAIgo()
    menuSize = MenuSize()
    playGame = Gaming()
    use_alpha_beta = menuAlgo.get_btnAnphaBeta().selected
    menu.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if SCREEN == Screen.MENUINTRO:
                SCREEN = menu.action(event)
                menu.draw()
            if SCREEN == Screen.MENUAI:
                SCREEN = menuAI.action(event)
                menuAI.drawMenu()
            elif SCREEN == Screen.SELECT_AIGO:
                SCREEN = menuAlgo.action(event, playGame, menuAI.get_btnAi().selected)
                use_alpha_beta = menuAlgo.get_btnAnphaBeta().selected
                menuAlgo.drawMenuAlgo()
            elif SCREEN == Screen.SELECT_SIZE:
                SCREEN = menuSize.action(event, playGame, menuAI.get_btnAi().selected, use_alpha_beta)
                menuSize.drawMenuSize()
            elif SCREEN == Screen.GAMING:
                SCREEN = playGame.action(event, menuAlgo)
                playGame.draw("Thuật toán cắt tỉa Alpha Beta" if use_alpha_beta else "Thuật toán Min_Max")
            elif SCREEN == Screen.MENUSIZEHUMAN:
                SCREEN = menuSizeHuman.action(event)
                menuSizeHuman.drawMenuSize()
            elif SCREEN == Screen.GAMINGHUMAN:
                play_game = menuSizeHuman.get_play_game() 
                if play_game:
                    SCREEN = play_game.action(event)
                    play_game.draw()
                    pygame.display.update()

        pygame.display.update()