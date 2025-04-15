import pygame
from OSCBackend import OSC_Backend
from  utils.input_utils import Inputs
from utils.animation_utils import Animator
from utils.sprite_utils import Sprite

class Module:

    def __init__(self):
        
        self.OSC_Communicator = OSC_Backend()

        self.Inputs = Inputs()

        self.Toggle = self.Inputs.Create_Button([0.25,0.25], [0.5,0.25], Ratio_Driven_Position = True)

        self.Toggle.Visibility = False



        # OSC Switch Animation and circle

        self.Animator = Animator()

        self.OSC_Switch_Circle = self.Animator.Create_Circle()

        self.OSC_Switch_Circle.Add_Frame([0.4,0.375], 0.075, [255,0,0],0)

        self.OSC_Switch_Circle.Add_Frame([0.6,0.375], 0.075, [0,255,0],0.3)





        #Osc Switch Backing

        self.OSC_Switch_Backing = pygame.image.load('./Assets/OSC_Toggle_Backing.png')

        self.OSC_Switch_Backing_Ratio = [0.2, 0.8, 0.25, 0.5]




        # Connection Status Sprite

        self.Connection_Sprite = Sprite()

        Images = ["./Assets/OSC_Off.png","./Assets/OSC_Searching.png","./Assets/OSC_Connected.png"]

        self.Connection_Sprite.Load_Images(Images)

        self.Connection_Sprite.Pos = [0,0.5]

        self.Connection_Sprite.Size = [1,0.5]




        

        self.Update_Vars = []

        self.Surface = None
        

    def Draw(self, Width, Height):

        Update_Vars = [Width, Height, self.OSC_Communicator.Device.Connected, self.OSC_Communicator.Searching]

        if not self.Update_Vars == Update_Vars or self.Inputs.Surface_Update or self.Animator.Play:

            Surface = pygame.Surface((Width, Height))

            Surface.fill((60,60,60))

            Blit_Pos = [self.OSC_Switch_Backing_Ratio[0]*Width, self.OSC_Switch_Backing_Ratio[2]*Height]

            Resize_Res = [round((self.OSC_Switch_Backing_Ratio[1]*Width)-Blit_Pos[0]), round((self.OSC_Switch_Backing_Ratio[3]*Height)-Blit_Pos[1])]
            

            OSC_Backing_Surface = pygame.transform.scale(self.OSC_Switch_Backing, Resize_Res)

            Surface.blit(OSC_Backing_Surface, Blit_Pos)

            Surface.blit(self.Inputs.Draw(Width, Height),[0,0])

            Surface.blit(self.Animator.Draw(Width, Height, True),[0,0])


            # OSC Connection Status Code

            try:
                if self.OSC_Communicator.Device.Connected:
                    self.Connection_Sprite.Sprite = 2
                elif self.OSC_Communicator.Searching:
                    self.Connection_Sprite.Sprite = 1
                else:
                    self.Connection_Sprite.Sprite = 0
            except:
                pass

            Surface.blit(self.Connection_Sprite.Draw(Width, Height),[0,0])

            
            

            self.Surface = Surface

            self.Update_Vars = Update_Vars

        return self.Surface

        


    def Update(self, Mouse, Keyboard = []):

        self.Inputs.Update(Mouse)

        self.OSC_Communicator.Connect_To_Device = self.Toggle.Value

        if self.Inputs.Surface_Update:

            self.Animator.Play_Animation(not self.Toggle.Value)

        
            


        




if __name__ == "__main__":
    from mouse_iterator import Mouse_Iterator
    

    
    Mouse = Mouse_Iterator()
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30
    pygame.display.set_caption("Manual")

    OSC_Module = Module()

    while True:

        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # All logic goes here

        #Update Mouse
        Mouse.Update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())


        #Input and update logic
        OSC_Module.Update(Mouse)

        
        #Draw Logic
        screen.blit(OSC_Module.Draw(width, height),[0,0])
        
        

       


        # flip display and clock tick
        pygame.display.flip()
        clock.tick(FPS)


