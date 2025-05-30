import pygame
import threading
from pythonosc import udp_client

def _detect_in_rect(pos, rect):
    if pos[0] >= rect[0] and pos[0] <= rect[0]+rect[2]: # x coord
        if pos[1] >= rect[1] and pos[1] <= rect[1]+rect[3]:
            return True
    return False

class Module:

    def __init__(self):

        from  utils.input_utils import Inputs

        self.Inputs = Inputs()

        self.Resolution = [200,200]

        self.Bar_Ratio = [0.4,0.15]

        self.Sent_Val = 0

        ip = "127.0.0.1"
        
        port = 8700

        self.client = udp_client.SimpleUDPClient(ip, port)

        self.Surface = None

        self.Slider = self.Inputs.Create_Slider([0.4,0.25], [0.2,0.5], Ratio_Driven_Position = True, Vertical = True)

        self.Update_Vars = []

    def Draw(self, Width, Height):

        Update_Vars = [Width, Height]

        redraw = False

        if not self.Update_Vars == Update_Vars:
            redraw = True
            self.Update_Vars = Update_Vars
            


        if self.Inputs.Surface_Update or redraw:

            Surface = pygame.Surface((Width, Height)) # Make Surface to draw on

            Surface.fill((60,60,60))

            Surface.blit(self.Inputs.Draw(Width, Height),[0,0])

            self.Surface = Surface
        else:
            Surface = self.Surface

        
        return Surface

        

        

    def Update(self, Mouse, Keyboard = []):

        self.Inputs.Update(Mouse, Keyboard)

        if not self.Slider.Value == self.Sent_Val:
            self.client.send_message("/vibrate", [self.Slider.Value,self.Slider.Value])
            self.Sent_Val = self.Slider.Value

            

                
                
            
        




if __name__ == "__main__":
    
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30

    pygame.display.set_caption("Manual")

    Manual_Controller = Module()


    while True:

        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        screen.fill((49,49,49))
        screen.blit(Manual_Controller.Draw(width, height),[0,0])

        Manual_Controller.Input(pygame.mouse.get_pos(),pygame.mouse.get_pressed())
        


        pygame.display.flip()
        clock.tick(FPS)

    

    
