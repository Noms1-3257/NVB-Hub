import pygame

class Module:

    def __init__(self):
        pass

    def Draw(self, Width, Height):
        pass

    def Update(self):
        pass




    
if __name__ == "__main__":
    import keyboard_iterator import Keyboard_Iterator
    import mouse_iterator import Mouse_Iterator

    Mouse = Mouse_Iterator()

    Keyboard = Keyboard_Iterator()
    
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30
    pygame.display.set_caption("Manual")

    while True:
        # update the mouse and keyboard
         Mouse.Update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
         Keyboard.Update()

        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # All logic goes here

        

        # flip display and clock tick
        pygame.display.flip()
        clock.tick(FPS)

    # quit logic

    pygame.quit()
