

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

def main():
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
        entityData = preGameLoop(entityData, screen)

        startFire(entityData)
        mainLoop(entityData, screen)
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

def basicInitialization():
    entitiesData = []
    for row in range(round(SCREEN_WIDTH / ENTITY_WIDTH)):
        entitiesData.append([])
        for col in range(round((SCREEN_HEIGHT - CONTROLS_HEIGHT)/ ENTITY_HEIGHT)):
            entitiesData[row].append([])          
            entitiesData[row][col].append(random.randrange(50, 100))
            entitiesData[row][col].append(0.2)
            entitiesData[row][col].append(0)
            entitiesData[row][col].append(0)


    return np.array(entitiesData)


def preGameLoop(entityData, screen):
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
                entityData = loadPreset(entityData)
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
        # Update Display
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
        # Lets you draw 
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
    y = random.randrange(0, int((SCREEN_HEIGHT-CONTROLS_HEIGHT)/ENTITY_HEIGHT))
    x = random.randrange(0, int(SCREEN_WIDTH/ENTITY_WIDTH))
    entityData[y][x][2] = 1


def mainLoop(entityData, screen):
    running = True
    print("FIRE STARTED")
    
    while running:
        t1 = time()
        prevEntityData = entityData
        
        # Handle quit
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False
        
        # Update fires
        entityData = updateFire(entityData)

        # Update display
        # Returns [(x, y, red, green, blue)]
        rects = []
        @jit(nopython=True, cache=True)
        def calcColors(entityData, prevEntityData):
            updateArr = []
            for x in range(entityData.shape[0]):
                for y in range(entityData.shape[1]):
                    # If it's not on fire, don't update
                    if entityData[x][y][2] == 0:
                        continue
                    
                    # Choose color based on entity type
                    if entityData[x][y][3] == 0:
                        updateArr.append((x, y, int(entityData[x][y][0]), 0, 0))
                    elif entityData[x][y][3] == 1:
                        updateArr.append((x, y, 50, 50, 50))
                    elif entityData[x][y][3] == 2:
                        updateArr.append((x, y, int(entityData[x][y][0]), 0, 0))
                    elif entityData[x][y][3] == 3:
                        updateArr.append((x, y, 0, 0, 200))
            return updateArr
        
        updateArr = calcColors(entityData, prevEntityData)

        # Update display with new pixels
        for update in updateArr:
            rect = Rect(update[1]*ENTITY_WIDTH, (update[0]*ENTITY_HEIGHT+CONTROLS_HEIGHT), ENTITY_WIDTH, ENTITY_HEIGHT)
            rects.append(rect)
            pygame.draw.rect(screen, (update[2], update[3], update[4]), rect) 
        pygame.display.update(rects)
    
        # Frame rate limiter
        while time()-t1 < SECOND_PER_FRAME_MIN:
            sleep(SECOND_PER_FRAME_MIN/5)


@jit(nopython=True)
def updateFire(entityData):
    # Iterate through all pixels
    for x in range(entityData.shape[0]):
        for y in range(entityData.shape[1]):
            # If the pixel isn't on fire, skip
            if entityData[x][y][2] == 0:
                continue
            
            # Burn some of the pixels fuel and make sure fuel isn't negative
            entityData[x][y][0] -= BURN_RATE
            if entityData[x][y][0] < 0:
                entityData[x][y][0] = 0
                entityData[x][y][2] = 0
    
            xOffset = FLAME_RADIUS

            # While the current xOffset is within flame radius 
            while xOffset > int(np.negative(FLAME_RADIUS)):
                yOffset = FLAME_RADIUS
                # Check that the element will actually exist
                if xOffset+x < 0:
                    break
                elif entityData.shape[0] <= xOffset+x:
                    xOffset -= 1
                    continue
                # While the current yOffset is within flame radius
                while yOffset > int(np.negative(FLAME_RADIUS)):
                    # Handle out of bounds and div by 0
                    if yOffset+y < 0:
                        break
                    elif entityData.shape[1] <= yOffset+y or (xOffset == 0 and yOffset == 0):
                        yOffset -= 1
                        continue
                    # If the target entity is already on fire or out of fuel, skip 
                    entityTwo = entityData[x+xOffset][y+yOffset]
                    if entityTwo[2] == 1 or entityTwo[0] <= 0:
                        yOffset -= 1
                        continue
                    
                    # Calculate distance between target and current pixel
                    distance = sqrt(pow(xOffset, 2) + pow(yOffset, 2))

                    # Determine how likely a entity is to be lit on fire
                    fireChance = (1 / (pow(distance, 3))) * entityTwo[1] 

                    # Check if the entity will get lit on fire and light it
                    val = random.random()
                    if  val <= fireChance:
                        entityTwo[2] = 1
                    yOffset -= 1
                xOffset -= 1
    
    return entityData


@jit(nopython=True, cache=True)
def numpyInitialization():
    # Calculate size of array and initialize it
    xEntities = (round(SCREEN_WIDTH / ENTITY_WIDTH))
    yEntities = (round((SCREEN_HEIGHT - CONTROLS_HEIGHT)/ENTITY_HEIGHT))
    entities = np.zeros((xEntities, yEntities, 4))

    # Fill array with grass with random fuel
    for row in range(entities.shape[0]):
        for col in range(entities.shape[1]):
            entities[row][col][0] = random.randrange(50, 100)
            entities[row][col][1] = 0.2
            entities[row][col][2] = 0
            entities[row][col][3] = 0

    return entities


def loadPreset(data):
    # get converted image from im_resize
    pixelArr = Ret.ret_arr(int(SCREEN_WIDTH/ENTITY_WIDTH), 'C:/Users/bryan/Documents/code/fire/fire-sim/pleasanton.jpg', True)
    @jit(nopython=True)
    def convertArray(arr, entityData):
        # Iterate over image array
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                # Determine conversion based on color
                if np.array_equal(arr[i][j] , [245,35,93]):
                    entityData[i][j][0] = 0
                    entityData[i][j][1] = 0
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 1
                elif np.array_equal(arr[i][j] , [135,145,148]):
                    entityData[i][j][0] = 200
                    entityData[i][j][1] = 0.05
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 2
                elif np.array_equal(arr[i][j] , [137,159,68]) or np.array_equal(arr[i][j] , [24,35,33]):
                    #make it a light green tree color
                    entityData[i][j][0] = random.randrange(50, 100)
                    entityData[i][j][1] = 0.2
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 0
                elif np.array_equal(arr[i][j] , [88,183,135]) or np.array_equal(arr[i][j] , [255,0,214]):
                    #make it a water color
                    entityData[i][j][0] = 0
                    entityData[i][j][1] = 0
                    entityData[i][j][2] = 0
                    entityData[i][j][3] = 3
        return entityData
    
    return convertArray(pixelArr, data)
  
        
if __name__ == "__main__":
    main()