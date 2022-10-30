

# Import the pygame module

from time import sleep
import pygame
import random
from math import sqrt
from button import Button
from im_resize import Ret
import numpy as np
from numba import jit, cuda
from timeit import default_timer as timer
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_s,
    K_l,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)



# Define constants for the screen width and height
CONTROLS_HEIGHT = 200
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = SCREEN_HEIGHT - CONTROLS_HEIGHT
FLAME_RADIUS = 3
ENTITY_WIDTH = 5
ENTITY_HEIGHT = ENTITY_WIDTH

SIMULATION_HEIGHT = SCREEN_HEIGHT - CONTROLS_HEIGHT

 # Define a player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, fuel, flamability):
        super(Entity, self).__init__()
        self.x = x
        self.y = y
        self.fuel = fuel
        self.flamability = flamability
        self.surf = pygame.Surface((ENTITY_WIDTH, ENTITY_HEIGHT))
        self.onFire = False
        self.rect = self.surf.get_rect()
    
    def setOnFire(self):
        self.onFire = True
        self.surf.fill((self.fuel, 0, 0))
    def burn(self):
        self.fuel -= random.randrange(0, 10)
        if self.fuel <= 0:
            self.onFire = False
            self.surf.fill((0, 0 , 0))
            return
        self.surf.fill((self.fuel, 0, 0))

class Tree(Entity):
    def __init__(self, x, y):
        fuel = random.randrange(50, 100)
        flamability = 0.1
        super(Tree, self).__init__(x, y, fuel, flamability)
        self.surf.fill((0, 155+self.fuel, 0))

class Water(Entity):
    def __init__(self, x, y):
        fuel = 0
        flamability = 0
        super(Water, self).__init__(x, y, fuel, flamability)
        self.surf.fill((65,105,225))

class Road(Entity):
    def __init__(self, x, y):
        fuel = 0
        flamability = 0
        super(Road, self).__init__(x, y, fuel, flamability)
        self.surf.fill((105,105,105))

class House(Entity):
    def __init__(self, x, y):
        fuel = 200
        flamability = 0.05
        super(House, self).__init__(x, y, fuel, flamability)
        self.surf.fill((150, 75, 0))
    
class FireBreak(Entity):
    def __init__(self, x, y):
        fuel = 10
        flamability = 0.01
        super(FireBreak, self).__init__(x, y, fuel, flamability)
        self.surf.fill((255, 255, 255))

def main():
    
    data = {}
    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create and populate tree list
    entities = basicInitialization()
    entities = startupLoop(entities, screen)
    startFire(entities)

    start = timer()
    mainLoop(entities, screen, data)
    print(timer()-start)

    print(data)

def basicInitialization():
    entities = []
    for i in range(round(SCREEN_WIDTH / ENTITY_WIDTH)):
        for k in range(round((SCREEN_HEIGHT - CONTROLS_HEIGHT)/ ENTITY_HEIGHT)):
            entities.append(Tree(i, k))
    return entities

def startupLoop(entities, screen):
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
            feedback="lol"
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
                return entities
            if buttonList[1].click(event):
                entities = loadPleasanton(entities)
                return entities
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

        # Lets you draw water
        if pygame.mouse.get_pressed()[0]:
            
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1] - CONTROLS_HEIGHT
            column = int(mouseX / ENTITY_WIDTH)
            row = int(mouseY / ENTITY_HEIGHT)
            if buttonList[2].on:  
                for i, entity in enumerate(entities):
                    if entity.x == column and entity.y == row:
                        entities.pop(i)
                        entities.append(Road(column, row))
            elif buttonList[3].on:
                for i, entity in enumerate(entities):
                    if entity.x == column and entity.y == row:
                        entities.pop(i)
                        entities.append(House(column, row))
            elif buttonList[4].on:
                for i, entity in enumerate(entities):
                    if entity.x == column and entity.y == row:
                        entities.pop(i)
                        entities.append(Water(column, row))
            elif buttonList[5].on:
                for i, entity in enumerate(entities):
                    if entity.x == column and entity.y == row:
                        entities.pop(i)
                        entities.append(FireBreak(column, row))
        
        for entity in entities:
            screen.blit(entity.surf, (entity.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entity.y * ENTITY_HEIGHT)) 

        for button in buttonList:
            button.show(screen)
        pygame.display.flip()

def startFire(entities):
    # entities[0].setOnFire()
    while True:
        randEntity = entities[random.randrange(0, len(entities))]
        if randEntity.flamability <= 0:
            continue
        randEntity.setOnFire()
        break

def mainLoop(entities, screen, data):
    data["flameCount"] = []    
    collectData = True
    # Main loop
    loopCount = 0
    running = True
    while running:
        if collectData:
            data["flameCount"].append(0)
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False
            

        # Fill the screen with black
        screen.fill((0, 0, 0))
        start = timer()
        # Draw the trees on the screen
        for index, entityOne in enumerate(entities):
         # If the current tree is not on fire, draw the tree as normal
            
            if not entityOne.onFire:
                screen.blit(entityOne.surf, (entityOne.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entityOne.y * ENTITY_HEIGHT))
                continue
            if collectData:
                data["flameCount"][loopCount] += 1
            entityOne.burn()

        #     # If the current tree is on fire, check if it lights other trees on fire
            # SCREEN_WIDTH / ENTITY_WIDTH gets the number of elements in a row
            currentRow = FLAME_RADIUS
            
            while currentRow > int(np.negative(FLAME_RADIUS)):
                currentCol = FLAME_RADIUS
                # print(f"col: {currentRow}")
                while currentCol > int(np.negative(FLAME_RADIUS)):
                    # print(f"row: {currentCol}")
                    entityTwoIndex = int(index + currentCol + currentRow * (SCREEN_WIDTH / ENTITY_WIDTH))
                    if len(entities) <= entityTwoIndex and entityTwoIndex > 0:
                        currentCol -= 1
                        continue
                    entityTwo = entities[entityTwoIndex]
                    currentCol -= 1
                    if entityTwo.onFire or entityTwo.fuel <= 0:
                        continue
                    # Calculate the distance between tree one and tree two 
                    dx = entityOne.x - entityTwo.x
                    dy = entityOne.y - entityTwo.y
                    distance = sqrt(pow(dx, 2) + pow(dy, 2))
                    if distance > 10:
                        continue

                    # Determine how likely a tree is to be lit on fire
                    fireChance = (1 / (pow(distance, 2))) * entityTwo.flamability 


                    # Check if the tree will get lit on fire
                    val = random.random()
                    if  val <= fireChance:
                        entityTwo.setOnFire()
                currentRow -= 1

            screen.blit(entityOne.surf, (entityOne.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entityOne.y * ENTITY_HEIGHT))
        

        # Update the display
        pygame.display.flip()
        print(f"Time:{timer()-start}")
        if collectData:
            if data["flameCount"][loopCount] == 0:
                collectData = False
        loopCount += 1
    

def loadPleasanton(entities):
    
    entities = []
    # arr = Ret.ret_arr(800)
    arr = Ret.ret_arr(int(SCREEN_WIDTH/ENTITY_WIDTH), show=True)
    for i, row in enumerate(arr):
        for j, col in enumerate(row):
            if np.array_equal(col , [255,255,255]):
                #make tile a road color 
                entities.append(Road(j, i))
                
            if np.array_equal(col , [135,145,148]):
                #make it a building colotemp = Road(row, col)
                entities.append(House(j, i))
                
            if np.array_equal(col , [137,159,68]):
                #make it a light green tree collor
                entities.append(Tree(j, i))
            if np.array_equal(col , [24,35,33]):
                #make it a darker green color
                entities.append(Tree(j, i))
            if np.array_equal(col , [88,183,135]) or np.array_equal(col , [255,0,214]):
                #make it a water color
                entities.append(Water(j, i))

    print(f"LENGTH: {len(entities)}")
    return entities
  
        
if __name__ == "__main__":
    main()