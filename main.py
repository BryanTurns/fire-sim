

# Import the pygame module

from time import sleep
from xmlrpc.client import Boolean
import pygame
import random
import pygame_menu #pip install this
from pygame_menu import themes
from math import sqrt, ceil
from button import Button
from im_resize import Ret
import numpy as np
from flameChart import graphData
from numba import jit, cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
from math import ceil, sqrt
from time import time

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import * 
# (
#     K_s,
#     K_l,
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
#     MOUSEBUTTONDOWN
# )


# Define constants for the screen width and height
CONTROLS_HEIGHT = 200
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = SCREEN_HEIGHT - CONTROLS_HEIGHT
FLAME_RADIUS = 3
ENTITY_WIDTH = 1
ENTITY_HEIGHT = ENTITY_WIDTH
BURN_RATE = 10
SECOND_PER_FRAME_MIN = 0.2

SIMULATION_HEIGHT = SCREEN_HEIGHT - CONTROLS_HEIGHT

 # Define a player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'
def main():
    
    data = {}
    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    flags = DOUBLEBUF
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=flags)
    screen.set_alpha(None)
    
    def start():
        menuRun = False
        pygame.display.quit()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=flags)
        entityData = numpyInitialization()
        entityData = startupLoop(entityData, screen)

        startFire(entityData)
        mainLoop(entityData, screen, data)
        graphData(data)
    #imported image
    myimage = pygame_menu.baseimage.BaseImage(
        image_path = "bush.jpg",
        drawing_mode = pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
    
    #Custom Theme
    mytheme= themes.THEME_GREEN.copy()
    mytheme.title_font = pygame_menu.font.FONT_8BIT
    mytheme.background_color = myimage
    mytheme.title_background_color = "black"
    mytheme.widget_background_color ="black"
    mytheme.widget_border_color = "white"
    mytheme.widget_border_width = 1
    mytheme.cursor_selection_color = "grey"

    #Menu    
    mainmenu = pygame_menu.Menu('Fire Simulation', SCREEN_WIDTH, 500, theme=mytheme)

    HELP = "Select a simulation\n"\
        "Protect the community from wildfires\n"\
        "Obstruct fires with water and roadworks\n"\
        "Flammability is calculated based on material"
    def help_():
        mainmenu._open(help_menu)
    mainmenu.add.button('Start Simulation', start, font_name = pygame_menu.font.FONT_MUNRO)
    mainmenu.add.button('Help', help_, font_name = pygame_menu.font.FONT_MUNRO)
    mainmenu.add.button('Quit', quit, font_name = pygame_menu.font.FONT_MUNRO)
    help_menu = pygame_menu.Menu('About', 600, 400, theme = mytheme)
    help_menu.add.label(HELP, max_char = -1, font_size = 20)
    menuRun = True
    while menuRun:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
    
        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(screen)

        pygame.display.update() 

def startupLoop(entityData, screen):
    rectArray = []
    buttonList = []
    buttonList.append(Button(
                "Basic Sim",
                (100,100),
                font=30,
                bg="blue",
                feedback="You clicked"))
    buttonList.append(Button(
            "Pleasanton Sim",
            (300, 100),
            font = 30, 
            bg="blue",
            feedback="Pleasanton Sim"
    ))
    buttonList.append(Button(
        "Road",
        (500, 100),
        font=30,
        bg="blue",
        feedback="Road"
    ))
    buttonList.append(Button(
        "House",
        (600, 100),
        font=30,
        bg="blue",
        feedback="House"
    ))
    buttonList.append(Button(
        "Water",
        (700, 100),
        font=30,
        bg="blue",
        feedback="Water"
    ))
    buttonList.append(Button(
        "Fire Break",
        (800, 100),
        font=30,
        bg="blue",
        feedback="Fire Break"
    ))

    pygame.display.flip()
    while True:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    pygame.quit()
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                pygame.quit()

            if buttonList[0].click(event):
                return entityData
            if buttonList[1].click(event):
                entityData = loadPleasanton(entityData)
                pygame.display.flip()
                # return entities
            if buttonList[2].click(event):
                for button in buttonList:
                    if button != buttonList[2] and button.on:
                        button.change_text(button.original, "blue")
                        button.on = False
            if buttonList[3].click(event):
                for button in buttonList:
                    if button != buttonList[3] and button.on:
                        button.change_text(button.original, "blue")
                        button.on = False
            if buttonList[4].click(event):
                for button in buttonList:
                    if button != buttonList[4] and button.on:
                        button.change_text(button.original, "blue")
                        button.on = False
            if buttonList[5].click(event):
                for button in buttonList:
                    if button != buttonList[5] and button.on:
                        button.change_text(button.original, "blue")
                        button.on = False
        for y, row in enumerate(entityData):
            rectArray.append([])
            for x, entity in enumerate(row):
                rect = Rect(x*ENTITY_WIDTH, y*ENTITY_HEIGHT+CONTROLS_HEIGHT, ENTITY_WIDTH, ENTITY_HEIGHT)
                rectArray[y].append(rect)
                if entity[3] == 0:
                    if entity[2] == 0:
                        if entity[0] == 0:
                            pygame.draw.rect(screen, (0, 0, 0), rect)
                        else:
                            pygame.draw.rect(screen, (0, 50+entity[0], 0), rect)
                    else:
                        pygame.draw.rect(screen, (entity[0], 0, 0), rect)
                if entity[3] == 1:
                    pygame.draw.rect(screen, (50, 50, 50), rect)
                if entity[3] == 2:
                    if entity[2] == 0:
                        if entity[0] == 0:
                            pygame.draw.rect(screen, (0, 0, 0), rect)
                        else:
                            pygame.draw.rect(screen, (150, 75, 0), rect)
                    else:
                        pygame.draw.rect(screen, (entity[0], 0, 0), rect)
                if entity[3] == 3:
                    pygame.draw.rect(screen, (0, 0, 200), rect)
        # Lets you draw water
        if pygame.mouse.get_pressed()[0]:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1] - CONTROLS_HEIGHT
            column = int(mouseX / ENTITY_WIDTH)
            row = int(mouseY / ENTITY_HEIGHT)
            if buttonList[2].on:  
                entityData[row][column][0] = 0
                entityData[row][column][1] = 0
                entityData[row][column][2] = 0
                entityData[row][column][3] = 1
            elif buttonList[3].on:
                entityData[row][column][0] = 200
                entityData[row][column][1] = 0.05
                entityData[row][column][2] = 0
                entityData[row][column][3] = 2
            elif buttonList[4].on:
                entityData[row][column][0] = 0
                entityData[row][column][1] = 0
                entityData[row][column][2] = 0
                entityData[row][column][3] = 3
            elif buttonList[5].on:
                entityData[row][column][0] = 0
                entityData[row][column][1] = 0
                entityData[row][column][2] = 0
                entityData[row][column][3] = 4        

        for button in buttonList:
            button.show(screen)
        

def startFire(entityData):
    while True:
        y = random.randrange(0, int((SCREEN_HEIGHT-CONTROLS_HEIGHT)/ENTITY_HEIGHT))
        x = random.randrange(0, int(SCREEN_WIDTH/ENTITY_WIDTH))
        entityData[y][x][2] = 1
        break
                      
def mainLoop(entityData, screen, data):
    data["flameCount"] = []    
    data["totalFireChance"] = []
    data["blocksBurned"] = []
    data["percentBurned"] = []
    data["numBlocks"] = len(entityData) * len(entityData[0])
    collectData = True
    # Main loop
    loopCount = 0
    running = True

    threadsperblock = (16, 16)
    blockspergrid_x = ceil(entityData.shape[0] / threadsperblock[0])
    blockspergrid_y = ceil(entityData.shape[1] / threadsperblock[1])
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    print(f"Blocks/grid: {blockspergrid} | Threads per Block {threadsperblock}")

    rng_states = create_xoroshiro128p_states(threadsperblock[0] * threadsperblock[1] *blockspergrid[0]* blockspergrid[1], seed=14575389)
    d_rng_states = cuda.to_device(rng_states)
    d_readarray = cuda.to_device(entityData)
    d_newarray = cuda.to_device(entityData)
    d_flameradius = FLAME_RADIUS
    d_burnrate = BURN_RATE

    firstRun = True
    while running:
        t1 = time()
        prevEntityData = entityData

        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False
            
        updateFireCuda[blockspergrid, threadsperblock](d_readarray, d_newarray, d_flameradius, d_burnrate, d_rng_states)
        d_readarray.copy_to_device(d_newarray) 
        entityData = d_newarray.copy_to_host()    

        rects = []
        @jit(nopython=True, cache=True)
        def testFunc(entityData, prevEntityData):
            testArr = []
            for y in range(entityData.shape[0]):
                for x in range(entityData.shape[1]):
                    if (entityData[y][x] == prevEntityData[y][x]).all():
                        continue
                    elif entityData[y][x][2] == 0:
                        continue

                    if entityData[y][x][3] == 0:
                        testArr.append((y, x, int(entityData[y][x][0]), 0, 0))
                    elif entityData[y][x][3] == 1:
                        testArr.append((y, x, 50, 50, 50))
                    elif entityData[y][x][3] == 2:
                        testArr.append((y, x, int(entityData[y][x][0]), 0, 0))
                    elif entityData[y][x][3] == 3:
                        testArr.append((y, x, 0, 0, 200))
            return testArr
        
        testArr = testFunc(entityData, prevEntityData)


        for item in testArr:
            rect = Rect(item[1]*ENTITY_WIDTH, (item[0]*ENTITY_HEIGHT+CONTROLS_HEIGHT), ENTITY_WIDTH, ENTITY_HEIGHT)
            rects.append(rect)
            pygame.draw.rect(screen, (item[2], item[3], item[4]), rect) 
        pygame.display.update(rects)
    
    
        while time()-t1 < SECOND_PER_FRAME_MIN:
            sleep(0.05)

@jit(nopython=True, cache=True)
def numpyInitialization():
    xEntities = (round(SCREEN_WIDTH / ENTITY_WIDTH))
    yEntities = (round((SCREEN_HEIGHT - CONTROLS_HEIGHT)/ENTITY_HEIGHT))
    entities = np.zeros((xEntities, yEntities, 4))

    for row in range(entities.shape[0]):
        for col in range(entities.shape[1]):
            entities[row][col][0] = random.randrange(50, 100)
            entities[row][col][1] = 0.2
            entities[row][col][2] = 0
            entities[row][col][3] = 0

    return entities

@cuda.jit(cache=True)
def updateFireCuda(readOnlyEntityData, newEntityData, flameRadius, burn_rate, rng_states):
    row, col = cuda.grid(2)

    if readOnlyEntityData[row][col][2] == 0:
        return
    
    newEntityData[row][col][0] -= burn_rate
    if newEntityData[row][col][0] < 0:
        newEntityData[row][col][0] = 0
        newEntityData[row][col][2] = 0

    yOffset = flameRadius
    while yOffset > -flameRadius:
        xOffset = flameRadius

        if readOnlyEntityData.shape[0] <= (yOffset + row) or (yOffset + row) < 0:
            yOffset -= 1
            continue

        while xOffset > -flameRadius:
            if readOnlyEntityData.shape[1] <= (xOffset + col) or (xOffset + col) < 0 or readOnlyEntityData[yOffset + row][xOffset + col][2] == 1 or readOnlyEntityData[yOffset + row][xOffset + col][0] <= 0:
                xOffset -= 1
                continue

            distance = sqrt(pow(xOffset, 2) + pow(yOffset, 2))

            fireChance = (1 / (pow(distance, 3))) * readOnlyEntityData[yOffset + row][xOffset+col][1]
            
            randomNum = xoroshiro128p_uniform_float32(rng_states, cuda.grid(1))
            if randomNum <= fireChance:
                newEntityData[yOffset + row][xOffset + col][2] = 1
            xOffset -= 1
        yOffset -= 1

def loadPleasanton(data):
    # arr = Ret.ret_arr(800)
    pixelArr = Ret.ret_arr(int(SCREEN_WIDTH/ENTITY_WIDTH), 'C:/Users/bryan/Documents/code/fire/fire-sim/red_pink.jpg', True)
    @jit(nopython=True)
    def convertArray(arr, entityData):
        for i, row in enumerate(arr):
            for j, col in enumerate(row):
                if np.array_equal(col , [245,35,93]):
                    entityData[i][j][0] = 0
                    entityData[i][j][1] = 0
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 1
                if np.array_equal(col , [135,145,148]):
                    #make it a building colotemp = Road(row, col)
                    entityData[i][j][0] = 200
                    entityData[i][j][1] = 0.05
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 2
                    
                if np.array_equal(col , [137,159,68]):
                    #make it a light green tree collor
                    entityData[i][j][0] = random.randrange(50, 100)
                    entityData[i][j][1] = 0.2
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 0

                if np.array_equal(col , [24,35,33]):
                    entityData[i][j][0] = random.randrange(50, 100)
                    entityData[i][j][1] = 0.2
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 0
                if np.array_equal(col , [88,183,135]) or np.array_equal(col , [255,0,214]):
                    #make it a water color
                    entityData[i][j][0] = 0
                    entityData[i][j][1] = 0
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 3
        return entityData
    
    return convertArray(pixelArr, data)
  
        
if __name__ == "__main__":
    main()