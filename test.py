

# Import the pygame module

from time import sleep
import pygame
import random
from math import sqrt
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_s,
    K_l,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)



# Define constants for the screen width and height
CONTROLS_HEIGHT = 200
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
ENTITY_WIDTH = 20
ENTITY_HEIGHT = 20

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
        self.surf.fill((self.fuel+ 100, 0, 0))


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
        flamability = 0
        super(House, self).__init__(x, y, fuel, flamability)

def main():
    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create and populate tree list
    entities = basicInitialization()
    startupLoop(entities, screen)
    startFire(entities)

    mainLoop(entities, screen)



def basicInitialization():
    entities = []
    for i in range(round(SCREEN_WIDTH / ENTITY_WIDTH)):
        for k in range(round((SCREEN_HEIGHT - CONTROLS_HEIGHT)/ ENTITY_HEIGHT)):
            entities.append(Tree(i, k))
    return entities

def startupLoop(entities, screen):
    while True:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    pygame.quit()
                elif event.key == K_s:
                    return
                elif event.key == K_l:
                    loadArray()
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                pygame.quit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
           
        
        if pygame.mouse.get_pressed()[0]:
            # print("Mouse Down!")
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1] - CONTROLS_HEIGHT
            # print(f"x:{mouseX} y:{mouseY}")
            column = int(mouseX / ENTITY_WIDTH)
            row = int(mouseY / ENTITY_HEIGHT)
            # print(f"Collumn: {column} row: {row}")
                
            for i, entity in enumerate(entities):
                if entity.x == column and entity.y == row:
                    entities.pop(i)
                    entities.append(Water(column, row))

        for entity in entities:
            screen.blit(entity.surf, (entity.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entity.y * ENTITY_HEIGHT)) 
        pygame.display.flip()

def startFire(entities):
    while True:
        randEntity = entities[random.randrange(0, len(entities))]
        if randEntity.flamability <= 0:
            continue
        randEntity.setOnFire()
        break

def mainLoop(entities, screen):
    # Main loop
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
            

        # Fill the screen with black
        screen.fill((255, 255, 255))
        # Draw the trees on the screen
        for entityOne in entities:
            # If the current tree is not on fire, draw the tree as normal

            if not entityOne.onFire:
                screen.blit(entityOne.surf, (entityOne.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entityOne.y * ENTITY_HEIGHT))
                continue
            entityOne.burn()
            # If the current tree is on fire, check if it lights other trees on fire
            for entityTwo in entities:
                # If the tree is already on fire, no need to see if it will be lit
                if entityTwo.onFire or entityTwo.fuel <= 0:
                    continue
                # Calculate the distance between tree one and tree two 
                dx = entityOne.x - entityTwo.x
                dy = entityOne.y - entityTwo.y
                distance = sqrt(pow(dx, 2) + pow(dy, 2))
                if distance > 10:
                    continue

                # Determine how likely a tree is to be lit on fire
                fireChance = (1 / (pow(distance, 4))) * entityTwo.flamability 

                # Check if the tree will get lit on fire
                val = random.random()
                if  val <= fireChance:
                    entityTwo.setOnFire()
            # Draw the current tree on screen
            screen.blit(entityOne.surf, (entityOne.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entityOne.y * ENTITY_HEIGHT))


        # Update the display
        pygame.display.flip()
    
def loadArray(array, entities):
    

    for row in array:
        for column in row:
            break

if __name__ == "__main__":
    main()