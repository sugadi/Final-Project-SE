import pygame
import sys
import os
from pygame.locals import *
import random

# time
currentTime = pygame.time.Clock()

# init pygame
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
inputFont = pygame.font.Font(None, 32)

# run the game at 60 frames per second
FPS = 100
velocity = 10
person_width = 5
person_height = 5

# direction
choices = ["up", "down", "left", "right"]

# color
alpha = (255, 255, 255)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
COLOR_INACTIVE = pygame.Color('blue')
COLOR_ACTIVE = pygame.Color('green')

# sound
pygame.mixer.init(44100, -16, 2, 2048)
game_sound = pygame.mixer.Sound("sound/surprise.mp3")
game_sound.set_volume(0.01)
celebration_sound = pygame.mixer.Sound("sound/puffy.mp3")
collision_sound_loader = pygame.mixer.Sound("sound/beeze.mp3")
game_sound.play()

# SCREEN
screen = pygame.display.set_mode((500, 500))

# write data
def record(filename, data):
    """
    :param filename: filename
    :param data: string
    :return: NONE
    """
    file = open(filename, "a")
    file.write(data)
    print("We Have Recorded User Data")

# write data
def recordRandom(data):
    """
    :param data: string
    :return: NONE
    """
    file = open("simulator.txt", "a")
    file.write(data)
    print("Simulation Data Recorded")

# reporter
def reporter(steps):
    """

    :param steps: a list of how many steps takes
    :return: NONE
    """
    print("Your highest steps:" + str(max(steps)))
    print("Your highest steps:" + str(min(steps)))
    print("Your average steps:" + str(sum(steps) / len(steps)))

def main_game():
    """
    Main Menu selection the functions
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wander in Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    click = False
    while True:
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "exit"', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        # rect( x, y, len, width)
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_4 = pygame.Rect(150, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                print("Game Menu")
                game_Menu()
        if button_2.collidepoint((mx, my)):
            if click:
                print("Options Menu")
                options()
        if button_4.collidepoint((mx, my)):
            if click:
                print("Simulation Menu")
                randomStimulationMenu()
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Start', font, (255, 255, 255), screen, 220, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Option', font, (255, 255, 255), screen, 220, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_4)
        text_data('Simulation', font, (255, 255, 255), screen, 220, 300)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        currentTime.tick(60)

# game engine
def text_data(text, font, color, surface, x, y):
    """
    :param text: text
    :param font: font attribute
    :param color: font color
    :param surface: the field text displayed on
    :param x: x-position
    :param y: y-position
    :return: NONE
    """
    font = pygame.font.Font('freesansbold.ttf', 20)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def displayGameOverWindow(gameWindow, gameOverImage, stepCounter):
    """
    :param stepCounter:
    :param gameWindow: window to display games
    :param gameOverImage: the image to display after game is over
    :return: NONE

    """
    game_sound.stop()
    pygame.mixer.Sound.play(celebration_sound)
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(str(stepCounter) + " steps", True, red, alpha)
    textRect = text.get_rect()
    start_time = pygame.time.get_ticks()
    pygame.display.set_caption("Congratulations, You have successfully completed the Game")
    while pygame.time.get_ticks() < start_time + 1000:
        gameWindow.fill(white)
        gameWindow.blit(gameOverImage, (0, 0))
        gameWindow.blit(text, textRect)
        pygame.display.update()
    celebration_sound.stop()
    main_game()


def first_player_movement(key_pressed, first_player_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param first_player_container: player 1 position
    :return: NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_a]:
        if first_player_container.x >= 5:
            first_player_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_d]:
        if first_player_container.x <= width - 50:
            first_player_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_w]:
        if first_player_container.y >= 5:
            first_player_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_s]:
        if first_player_container.y <= height - 50:
            first_player_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def second_player_movement(key_pressed, second_player_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param second_player_container: player 2 position
    :return:NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_LEFT]:
        if second_player_container.x >= 5:
            second_player_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_RIGHT]:
        if second_player_container.x <= width - 50:
            second_player_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_UP]:
        if second_player_container.y >= 5:
            second_player_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_DOWN]:
        if second_player_container.y <= height - 50:
            second_player_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def third_player_movement(key_pressed, third_player_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param third_player_container: player 3 position
    :return:NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_3]:
        if third_player_container.x >= 5:
            third_player_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_4]:
        if third_player_container.x <= width - 50:
            third_player_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_1]:
        if third_player_container.y >= 5:
            third_player_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_2]:
        if third_player_container.y <= height - 50:
            third_player_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def forth_player_movement(key_pressed, forth_player_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param forth_player_container: player 3 position
    :return:NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_8]:
        if forth_player_container.x >= 5:
            forth_player_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_9]:
        if forth_player_container.x <= width - 50:
            forth_player_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_6]:
        if forth_player_container.y >= 5:
            forth_player_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_7]:
        if forth_player_container.y <= height - 50:
            forth_player_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def game_Menu():
    """

    Game Option Panel
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('Press ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Please Select Game Mode', font, (255, 255, 255), screen, 20, 50)

        # mouse position
        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                k2_game()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                multiPlayerGameMenu()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data("Basic Game", font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Multiple Player', font, (255, 255, 255), screen, 180, 200)
        

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def k2_game():
    """

    Game Option Panel
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select Level Of Difficulty', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)
        button_4 = pygame.Rect(150, 400, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                simpleMode()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                moderateMode()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                complexMode()
        if button_4.collidepoint((mx, my)):
            if gameClick:
                complicateMode()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('simple', font, (255, 255, 255), screen, 220, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('moderate', font, (255, 255, 255), screen, 220, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('complex', font, (255, 255, 255), screen, 220, 300)
        pygame.draw.rect(screen, (0, 0, 128), button_4)
        text_data('complicate', font, (255, 255, 255), screen, 220, 400)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def displayGameWindow(gameWindow, forrestImage, first_player_container, second_player_container, person_One_Image,
                      person_Two_Image, ):
    """
    Display and update 2 players on the map
    :param forrestImage: forrest image
    :param person_Two_Image: display person one image
    :param person_One_Image: display person two image
    :param gameWindow: game window
    :param first_player_container: first_player position
    :param second_player_container: second_player position
    :return: NONE

    """
    gameWindow.fill(white)
    gameWindow.blit(forrestImage, (0, 0))
    gameWindow.blit(person_One_Image, (first_player_container.x, first_player_container.y))
    gameWindow.blit(person_Two_Image, (second_player_container.x, second_player_container.y))
    pygame.display.update()


def displayGameWindow_player3(gameWindow, forrestImage, first_player_container, second_player_container,
                              third_player_container, person_One_Image,
                              person_Two_Image, person_Three_Image):
    """
    Display and update 3 players on the map
    

    """
    gameWindow.fill(white)
    gameWindow.blit(forrestImage, (0, 0))
    gameWindow.blit(person_One_Image, (first_player_container.x, first_player_container.y))
    gameWindow.blit(person_Two_Image, (second_player_container.x, second_player_container.y))
    gameWindow.blit(person_Three_Image, (third_player_container.x, third_player_container.y))
    pygame.display.update()


def displayGameWindow_player4(gameWindow, forrestImage, first_player_container, second_player_container,
                              third_player_container, forth_player_container, person_One_Image,
                              person_Two_Image, person_Three_Image, person_Four_Image):
    """
    Display and update 4 players on the map
    
    

    """
    gameWindow.fill(white)
    gameWindow.blit(forrestImage, (0, 0))
    gameWindow.blit(person_One_Image, (first_player_container.x, first_player_container.y))
    gameWindow.blit(person_Two_Image, (second_player_container.x, second_player_container.y))
    gameWindow.blit(person_Three_Image, (third_player_container.x, third_player_container.y))
    gameWindow.blit(person_Four_Image, (forth_player_container.x, forth_player_container.y))
    pygame.display.update()


def simpleMode():
    """

    :return: simple mode active
    """

    print("simple Mode Selected")
    map300_manuelStimulation()


def map300_manuelStimulation():
    """

    stimulate the k_2 student Wandering In Woods game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init position and draw player
    gameOverImage = pygame.image.load(os.path.join('images', "300game.jpg"))
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50:
                filename = "results/simpleresults.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def moderateMode():
    """

    :return: simple mode active
    """
    print("moderate Mode Selected")
    map500_manuelStimulation()


def map500_manuelStimulation():
    """

    stimulate the k_2 student Wandering In Woods game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "500gameover.jpg"))

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50:
                filename = "results/moderateresults.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def complexMode():
    """

    :return: complex mode active
    """
    print("complex Mode Selected")
    vanGogh_Map_manuelStimulation()


def vanGogh_Map_manuelStimulation():
    """

    stimulate the k_2 student Wandering In Woods game
    :return: NONE

    """

    # map data
    width, height = 1200, 800
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "vanmap.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "forrestgameover.jpg"))

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50:
                filename = "results/complexresults.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def complicateMode():
    """

    :return: complicate mode active
    """
    print("complicate Mode Selected")
    Map2560_manuelStimulation()


def Map2560_manuelStimulation():
    """

    stimulate the k_2 student Wandering In Woods game
    :return: NONE

    """
    # map data
    width, height = 2560, 1600
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "2560map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "2560gameover.jpg"))

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50:
                filename = "results/complicateresults.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def k_3To5_game():
    """

    stimulate the k3-5 student Wandering In Woods game
    :return: NONE

    """
    # map data
    while True:
        try:
            width = int(input('Enter your width(0-1000):'))
            if width in range(0, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(0-1000): '))
            if height in range(0, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "300game.jpg"))

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50:
                Data = str(width) + " * " + str(height) + ":          " + str(stepCounter) + "   two player\n"
                filename = "results/randomMap.txt"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def multiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                map300_manuelStimulation()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                map300_manuelStimulation_3players()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                map300_manuelStimulation_4players()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def map300_manuelStimulation_3players():
    """

    stimulate the k_2 student Wandering In Woods game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    gameOverImage = pygame.image.load(os.path.join('images', "300game.jpg"))
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                first_player_container.y - second_player_container.y) <= 50 and abs(
                first_player_container.y - third_player_container.y) <= 50:
                filename = "results/simpleresults.txt"
                Data = str(stepCounter) + "  three players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        third_player_movement(key_pressed, third_player_container, stepCounter, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def map300_manuelStimulation_4players():
    """

    stimulate the k_2 student Wandering In Woods game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "green.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    gameOverImage = pygame.image.load(os.path.join('images', "300game.jpg"))
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)
    forth_player_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                first_player_container.x - forth_player_container.x) <= 50 and abs(
                first_player_container.y - second_player_container.y) <= 50 and abs(
                first_player_container.y - third_player_container.y) <= 50 and abs(
                first_player_container.y - forth_player_container.y) <= 50:
                filename = "results/simpleresults.txt"
                Data = str(stepCounter) + "  four players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_movement(key_pressed, first_player_container, stepCounter, width, height)
        second_player_movement(key_pressed, second_player_container, stepCounter, width, height)
        third_player_movement(key_pressed, third_player_container, stepCounter, width, height)
        forth_player_movement(key_pressed, forth_player_container, stepCounter, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  forth_player_container=forth_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


# option
def options():
    """

    :return: option page
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    optionClick = False
    running = True
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select Sound Volume', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if optionClick:
                set_Volume_Low()
        if button_2.collidepoint((mx, my)):
            if optionClick:
                set_Volume_moderate()
        if button_3.collidepoint((mx, my)):
            if optionClick:
                set_Volume_High()

        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Volume Low', font, (255, 255, 255), screen, 180, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Volume moderate', font, (255, 255, 255), screen, 180, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('Volume High', font, (255, 255, 255), screen, 180, 300)

        optionClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    optionClick = True

        pygame.display.update()
        currentTime.tick(60)


def set_Volume_Low():
    """
    change volume to Low
    :return: NONE
    """
    game_sound.set_volume(0.01)


def set_Volume_moderate():
    """
    change volume to moderate
    :return: NONE
    """
    game_sound.set_volume(0.1)


def set_Volume_High():
    """
    change volume to High
    :return: NONE
    """
    game_sound.set_volume(0.5)


def credit():
    """
    Display credit page
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    while True:
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('Credit:', font, (255, 255, 255), screen, 20, 20)
        text_data('CPSC 60500', font, (255, 255, 255), screen, 20, 50)
        text_data('Dr. Fadi Wedyan', font, (255, 255, 255), screen, 20, 80)
        text_data('Wandering in the Woods', font, (255, 255, 255), screen, 20, 110)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()

        pygame.display.update()
        currentTime.tick(60)


# random stimulation engine
def randomStimulationMenu():
    """
    Display random Stimulation Menu
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    game_sound.set_volume(0.01)
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    click = False
    while True:
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "exit"', font, (255, 255, 255), screen, 20, 20)
        text_data('Random Simulation'
                  ' Mode', font, (255, 255, 255), screen, 20, 50)
        mx, my = pygame.mouse.get_pos()

        # rect( x, y, len, width)
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                print("simple Simulation")
                stimulation_simple_MultiPlayerGameMenu()
        if button_2.collidepoint((mx, my)):
            if click:
                print("moderate Simulation")
                stimulation_Moderate_MultiPlayerGameMenu()
        if button_3.collidepoint((mx, my)):
            if click:
                print("complex Simulation")
                stimulation_Complex_MultiPlayerGameMenu()
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('simple', font, (255, 255, 255), screen, 220, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('moderate', font, (255, 255, 255), screen, 220, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('complex', font, (255, 255, 255), screen, 210, 300)
        

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        currentTime.tick(60)


def first_player_random_movement(first_player_Container, width, height):
    """

    :param height: window height
    :param width: window width
    :param first_player_Container: player 1 location update after move a step
    :return: NONE
    """
    choice = random.choice(choices)

    if choice == "left":
        if first_player_Container.x >= 50:
            first_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and first_player_Container.x <= width:
        if first_player_Container.x <= width - 50:
            first_player_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if first_player_Container.y >= 50:
            first_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        first_player_Container.y -= velocity

    if choice == "down":
        if first_player_Container.y <= height - 50:
            first_player_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def second_player_random_movement(second_player_Container, width, height):
    """

    :param second_player_Container:  player two container
    :param height: window height
    :param width: window width
    :return: NONE

    """
    choice = random.choice(choices)
    if choice == "left":
        if second_player_Container.x >= 50:
            second_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and second_player_Container.x <= width - 50:
        if second_player_Container.x <= width - 50:
            second_player_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if second_player_Container.y >= 50:
            second_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        second_player_Container.y -= velocity

    if choice == "down":
        if second_player_Container.y <= height - 50:
            second_player_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def third_player_random_movement(third_player_Container, width, height):
    """

    :param third_player_Container:  player three container
    :param height: window height
    :param width: window width
    :return: NONE

    """
    choice = random.choice(choices)
    if choice == "left":
        if third_player_Container.x >= 50:
            third_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and third_player_Container.x <= width - 50:
        if third_player_Container.x <= width - 50:
            third_player_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if third_player_Container.y >= 50:
            third_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        third_player_Container.y -= velocity

    if choice == "down":
        if third_player_Container.y <= height - 50:
            third_player_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def fourth_player_random_movement(forth_player_Container, width, height):
    """

    :param forth_player_Container:  player three container
    :param height: window height
    :param width: window width
    :return: NONE

    """
    choice = random.choice(choices)
    if choice == "left":
        if forth_player_Container.x >= 50:
            forth_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and forth_player_Container.x <= width - 50:
        if forth_player_Container.x <= width - 50:
            forth_player_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if forth_player_Container.y >= 50:
            forth_player_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        forth_player_Container.y -= velocity

    if choice == "down":
        if forth_player_Container.y <= height - 50:
            forth_player_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def stimulation_simple_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_simple()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_simple_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_simple_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def random_stimulation_simple():
    """
    Random Stimulate map size of 300 * 300
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 100 and abs(
                    first_player_container.y - second_player_container.y) <= 100:
                Data = "300 " + str(stepCounter) + " 2players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_simple_3player():
    """
    Random Stimulate map size of 300 * 300 for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50:
                Data = "300 " + str(stepCounter) + " 3players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(first_player_container.x)
        print(first_player_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_simple_4player():
    """
    Random Stimulate map size of 300 * 300 for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "green.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)
    forth_player_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.x - forth_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50 and abs(
                    first_player_container.y - forth_player_container.y) <= 50:
                Data = "300 " + str(stepCounter) + " 4players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(first_player_container.x)
        print(first_player_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        fourth_player_random_movement(forth_player_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  forth_player_container=forth_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


def stimulation_Moderate_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_moderate()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_moderate_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_moderate_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def random_stimulation_moderate():
    """
    Random Stimulate map size of 500 * 500
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init player position and draw them
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 100 and abs(
                    first_player_container.y - second_player_container.y) <= 100:
                Data = "500 " + str(stepCounter) + " 2players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_moderate_3player():
    """
    Random Stimulate map size of 500 * 500 for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50:
                Data = "500 " + str(stepCounter) + " 3players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(first_player_container.x)
        print(first_player_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_moderate_4player():
    """
    Random Stimulate map size of 500 * 500 for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "green.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)
    forth_player_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.x - forth_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50 and abs(
                    first_player_container.y - forth_player_container.y) <= 50:
                Data = "500         " + str(stepCounter) + "   4players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(first_player_container.x)
        print(first_player_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        fourth_player_random_movement(forth_player_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  forth_player_container=forth_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


def stimulation_Complex_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_complex()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_complex_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_complex_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def random_stimulation_complex():
    """
    Random Stimulate map size of 1000 * 1000
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 1000, 1000
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init player position and draw them
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 100 and abs(
                    first_player_container.y - second_player_container.y) <= 100:
                Data = "1000 " + str(stepCounter) + " 2players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_complex_3player():
    """
    Random Stimulate map size of complex for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 1000, 1000
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50:
                Data = "1000 " + str(stepCounter) + " 3players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_complex_4player():
    """
    Random Stimulate map size of complex for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "green.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)
    forth_player_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.x - forth_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50 and abs(
                    first_player_container.y - forth_player_container.y) <= 50:
                Data = "1000 " + str(stepCounter) + " 4players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        fourth_player_random_movement(forth_player_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  forth_player_container=forth_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


def stimulation_cusblueizedMap_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('Wandering In Woods')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menu.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        text_data('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        text_data('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_userDefined()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_userDefined_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_userDefined_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        text_data('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        text_data('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        text_data('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        currentTime.tick(60)


def random_stimulation_userDefined():
    """
    Random Stimulate map with cusblueized size
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    while True:
        try:
            width = int(input('Enter your width(200-1000):'))
            if width in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(200-1000): '))
            if height in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init player position and draw them
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 100 and abs(
                    first_player_container.y - second_player_container.y) <= 100:
                Data = str(width)+"*"+str(height) + "          " + str(stepCounter) + " 2player\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        displayGameWindow(gameWindow,
                          first_player_container=first_player_container,
                          forrestImage=forrestImage,
                          second_player_container=second_player_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_userDefined_3player():
    """
    Random Stimulate map with cusblueized size for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    while True:
        try:
            width = int(input('Enter your width(200-1000):'))
            if width in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(200-1000): '))
            if height in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50:
                Data = str(width)+"*"+str(height) + "          " + str(stepCounter) + " 3player\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_userDefined_4player():
    """
    Random Stimulate map with cusblueized size for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    """
        Random Stimulate map with cusblueized size
        :return: NONE
        """
    pygame.init()
    pygame.mixer.init()

    # map data
    while True:
        try:
            width = int(input('Enter your width(200-1000):'))
            if width in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(200-1000): '))
            if height in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "blue.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "red.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "violet.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "green.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    first_player_container = pygame.Rect(0, 0, person_width, person_height)
    second_player_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    third_player_container = pygame.Rect(0, height - 70, person_width, person_height)
    forth_player_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(first_player_container.x - second_player_container.x) <= 50 and abs(
                    first_player_container.x - third_player_container.x) <= 50 and abs(
                    first_player_container.x - forth_player_container.x) <= 50 and abs(
                    first_player_container.y - second_player_container.y) <= 50 and abs(
                    first_player_container.y - third_player_container.y) <= 50 and abs(
                    first_player_container.y - forth_player_container.y) <= 50:
                Data = str(width) + "*" + str(height) + "          " + str(stepCounter) + " 4player\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        first_player_random_movement(first_player_container, width, height)
        second_player_random_movement(second_player_container, width, height)
        third_player_random_movement(third_player_container, width, height)
        fourth_player_random_movement(forth_player_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  first_player_container=first_player_container,
                                  second_player_container=second_player_container,
                                  third_player_container=third_player_container,
                                  forth_player_container=forth_player_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )

main_game()
