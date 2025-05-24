import pygame
import copy
try:
    from Modules.RmCt.room_utils import Room
except:
    from room_utils import Room
from pythonosc import udp_client

class Module:

    def __init__(self):
        from  utils.input_utils import Inputs

        ip = "127.0.0.1"
        port = 8700
        self.client = udp_client.SimpleUDPClient(ip, port)

        # init the inputs
        self.Inputs = Inputs()

        # Room Connection
        self.RoomClient = Room()

        self.SentValue = 0

        # setup the connect button
        self.Toggle = self.Inputs.Create_Button([0.25,0.1], [0.5,0.1], Ratio_Driven_Position = True)
        self.ToggleOldValue = False
        
        # setup the text box for showing the room code
        self.Prompt = self.Inputs.Create_TextPrompt(Pos = [0.15,0.4],
                                                    Size = [0.7,0.2],
                                                    Ratio_Driven_Position = True,
                                                    CenterText=True)
        self.Prompt.Interactable = False

        

        
        
        # --- Drawing Vars ---

        self.Surface = None

        self.DrawUpdateVars = []


    def Draw(self, Width, Height):

        DrawUpdateVars = [Width, Height, self.Toggle.Value, self.Prompt.Text]

        if not DrawUpdateVars == self.DrawUpdateVars:

            self.Surface = pygame.Surface((Width, Height))

            self.Surface.fill((0,0,0,0))

            self.Surface.blit(self.Inputs.Draw(Width, Height),[0,0])

            self.DrawUpdateVars = copy.deepcopy(DrawUpdateVars)

        return self.Surface

    def Update(self, Mouse, Keyboard):

        # update the inputs
        
        self.Inputs.Update(Mouse,Keyboard)

        # Toggle a room

        if not self.Toggle.Value == self.ToggleOldValue:

            if self.Toggle.Value:
                self.RoomClient.start()
            else:
                self.RoomClient.stop()

            self.ToggleOldValue = self.Toggle.Value

        # handle sending vibration updates

        if not self.RoomClient.Values[0] == self.SentValue:
            print("sending change")
            self.client.send_message("/vibrate", [self.RoomClient.Values[0],self.RoomClient.Values[0]])
            self.SentValue = self.RoomClient.Values[0]
        self.Prompt.Text = self.RoomClient.RoomCode

        




    
if __name__ == "__main__":
    from keyboard_iterator import Keyboard_Iterator
    from mouse_iterator import Mouse_Iterator

    Mouse = Mouse_Iterator()

    Keyboard = Keyboard_Iterator()
    
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30
    pygame.display.set_caption("Manual")

    # init the module

    RmcModule = Module()
    RUN = True
    while RUN:
        
        # update the mouse and keyboard
        Mouse.Update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        Keyboard.Update()

        
        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            if event.type == pygame.QUIT: # End Quit Routine
                RUN = False
        # All logic goes here

        RmcModule.Update(Mouse, Keyboard)

        screen.blit(RmcModule.Draw(width, height), [0,0])

        

        

        # flip display and clock tick
        pygame.display.flip()
        clock.tick(FPS)

    # quit logic

    pygame.quit()
