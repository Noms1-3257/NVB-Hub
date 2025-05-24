import pygame
from OSCBackend import OSC_Backend
from  utils.input_utils import Inputs
from utils.animation_utils import Animator
from utils.sprite_utils import Sprite
import multiprocessing
from multiprocessing import Value as Shared_Process_Value
import time





def OSC_Comm_Process(Toggle_Value, Status_Queue, PROCESS_KILLFLAG):

    

    OSC_Communicator = OSC_Backend()

    while not PROCESS_KILLFLAG.value:

        if Toggle_Value.value:
            OSC_Communicator.Connect_To_Device = True
        else:
            OSC_Communicator.Connect_To_Device = False

        Status_Queue.put([OSC_Communicator.Searching, OSC_Communicator.Connected])
        
        time.sleep(0.1) # Update rate of the value changing stuff

    
    



class Module:

    def __init__(self):

        multiprocessing.freeze_support()

        # Setup the OSC process to improce performance

        self.Conn_Status = [False,False]

        self.OSC_Comm_Toggle = Shared_Process_Value("b", False)

        self.PROCESS_KILLFLAG = Shared_Process_Value("b", False)

        self.Status_Queue = multiprocessing.Queue()

        self.OSC_Args = (self.OSC_Comm_Toggle, self.Status_Queue,self.PROCESS_KILLFLAG)

        
        # Init and handle inputs

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

    def _Init_And_Start_Worker(self):
        self.OSC_Process = multiprocessing.Process(target=OSC_Comm_Process,name="NVB_OSC_Backend" ,args=self.OSC_Args)

        self.OSC_Process.daemon = True

        self.OSC_Process.start()

    def _Stop(self):
        self.PROCESS_KILLFLAG.value = True

    def Draw(self, Width, Height):

        Update_Vars = [Width, Height, self.Conn_Status]

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
                if self.Conn_Status[1]:
                    self.Connection_Sprite.Sprite = 2
                elif self.Conn_Status[0]:
                    self.Connection_Sprite.Sprite = 1
                else:
                    self.Connection_Sprite.Sprite = 0
            except:
                pass

            Surface.blit(self.Connection_Sprite.Draw(Width, Height),[0,0])

            
            

            self.Surface = Surface

            self.Update_Vars = Update_Vars

        return self.Surface

        


    def Update(self, Mouse, Keyboard):

        self.Inputs.Update(Mouse, Keyboard)

        self.OSC_Comm_Toggle.value = self.Toggle.Value

        

        while not self.Status_Queue.empty():
            self.Conn_Status = self.Status_Queue.get()

        

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


