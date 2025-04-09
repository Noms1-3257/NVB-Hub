import pygame

class Module:

    def __init__(self):
        pass

    def Draw(self, Width, Height):
        pass

    def Update(self):
        pass




    
if __name__ == "__main__":
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30
    pygame.display.set_caption("Manual")

    while True:

        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # All logic goes here


    # flip display and clock tick
    pygame.display.flip()
    clock.tick(FPS)
