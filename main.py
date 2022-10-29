

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
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
TREE_WIDTH = 10
TREE_HEIGHT = 10
 # Define a player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'
class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Tree, self).__init__()
        self.x = x 
        self.y = y
        self.surf = pygame.Surface((TREE_WIDTH, TREE_HEIGHT))
        # Random amount of fuel
        self.fuel = random.randrange(50, 100)
        # Determine tree color based off fuel amount
        self.surf.fill((0, 155+self.fuel, 0))
        self.image= pygame.image.load("C:/Users/bryan/Downloads/tree.png")
        self.rect = self.surf.get_rect()
        self.flamability = 0.1
        self.onFire = False
    
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

    
def main():
    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create and populate tree list
    trees = []
    for i in range(round(SCREEN_WIDTH / TREE_WIDTH)):
        for k in range(round(SCREEN_HEIGHT / TREE_HEIGHT)):
            trees.append(Tree(i, k))

    # Variable to keep the main loop running
    running = True

    trees[0].setOnFire()

    # Main loop
    while running:
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
        print("New game cycle")
        # Draw the trees on the screen
        for treeOne in trees:
            # If the current tree is not on fire, draw the tree as normal
            if not treeOne.onFire:
                screen.blit(treeOne.surf, (treeOne.x*TREE_WIDTH, treeOne.y * TREE_HEIGHT))
                continue
            print(f"x:{treeOne.x}, y:{treeOne.y}, fuel:{treeOne.fuel}")
            treeOne.burn()
            # If the current tree is on fire, check if it lights other trees on fire
            for treeTwo in trees:
                # If the tree is already on fire, no need to see if it will be lit
                if treeTwo.onFire or treeTwo.fuel <= 0:
                    continue
                # Calculate the distance between tree one and tree two 
                dx = treeOne.x - treeTwo.x
                dy = treeOne.y - treeTwo.y
                distance = sqrt(pow(dx, 2) + pow(dy, 2))

                # Determine how likely a tree is to be lit on fire
                fireChance = (1 / (pow(distance, 4))) * treeTwo.flamability 

                # Check if the tree will get lit on fire
                val = random.random()
                if  val <= fireChance:
                    treeTwo.setOnFire()
            # Draw the current tree on screen
            screen.blit(treeOne.surf, (treeOne.x*TREE_WIDTH, treeOne.y * TREE_HEIGHT))

        sleep(1)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()