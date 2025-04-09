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

        self.Value = 0

        self.Resolution = [200,200]

        self.Bar_Ratio = [0.4,0.15]

        self.Sent_Val = 0

        ip = "127.0.0.1"
        
        port = 8700

        self.client = udp_client.SimpleUDPClient(ip, port)

        self.Surface = None

    def Draw(self, Width, Height):

        New_Draw = False

        if not self.Resolution[0] == Width:
            self.Resolution[0] = Width
            New_Draw = True
        if not self.Resolution[1] == Height:
            self.Resolution[1] = Height
            New_Draw = True

        if New_Draw:

            Surface = pygame.Surface((Width, Height)) # Make Surface to draw on

            Surface.fill((60,60,60))

            self.Surface = Surface
        else:
            Surface = self.Surface

        Ratios = self.Bar_Ratio # Grab the ratio

        LeftRight = [Width*Ratios[0],Width*(1-Ratios[0])] # L and R Input bar coords

        UpDown = [Height*Ratios[1], Height*(1-Ratios[1])] # U and D Input bar coords

        
        # Input bar rect
        Main_Shape = [LeftRight[0],UpDown[0],(LeftRight[1]-LeftRight[0]), (UpDown[1]-UpDown[0])]

        # Draw that bitch
        pygame.draw.rect(Surface, (120,120,120), Main_Shape)



        Offset = UpDown[0]
        Value_Multipule = UpDown[1]-UpDown[0]

        Teller_Y_Coord = (Value_Multipule*(1-self.Value))+Offset

        pygame.draw.line(Surface, (200,30,20), (LeftRight[0],Teller_Y_Coord),(LeftRight[1],Teller_Y_Coord),3)

        return Surface

        

        

    def Update(self, Mouse):

        if Mouse.Held[0]:

            Width, Height = self.Resolution
            
            Ratios = self.Bar_Ratio

            LeftRight = [Width*Ratios[0],Width*(1-Ratios[0])]

            UpDown = [Height*Ratios[1], Height*(1-Ratios[1])]

            Main_Shape = [LeftRight[0],UpDown[0],(LeftRight[1]-LeftRight[0]), (UpDown[1]-UpDown[0])]

            if _detect_in_rect([Mouse.Pos[0],Mouse.Pos[1]], Main_Shape):

                Offset = UpDown[0]

                Mouse_Y = Mouse.Pos[1]

                Mouse_Y -= Offset

                Value_Multipule = UpDown[1]-Offset

                self.Value = 1-(Mouse_Y/Value_Multipule)

        if not self.Value == self.Sent_Val:
            self.client.send_message("/vibrate", [self.Value,self.Value])
            self.Sent_Val = self.Value

            

                
                
            
        




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


        screen.blit(Manual_Controller.Draw(width, height),[0,0])

        Manual_Controller.Input(pygame.mouse.get_pos(),pygame.mouse.get_pressed())
        


        pygame.display.flip()
        clock.tick(FPS)

    

    
