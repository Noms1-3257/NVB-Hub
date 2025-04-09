import pygame
from OSCBackend import OSC_Backend

def _smooth_value_list(value, data, flip=False):
    if flip:
        value = 1-value

    value_2 = 1-value

    return (value*data[0])+(value_2*data[1])

def _detect_in_rect(pos, rect):
    if pos[0] >= rect[0] and pos[0] <= rect[0]+rect[2]: # x coord
        if pos[1] >= rect[1] and pos[1] <= rect[1]+rect[3]:
            return True
    return False

class Module:

    def __init__(self):
        self._OSC_Toggle = False
        self._OSC_Toggle_Pos_Ratio = [0.2,0.3,0.2] # OSC Toggle switch ratio, aka, its position and size within the window
        self._OSC_Toggle_Rect = [1,1,1,1]
        self._OSC_Switch_Animation_Value = 0
        self._OSC_Switch_Animation_Speed = 10
        self._OSC_Switch_Rect_Pos = [0,0,10,10]
        self._OSCGUI_Surface = None
        self._OSC_New_Draw = True
        self._OSC_Indicator_Colors = [[10,255,10], [255,10,10]]
        self._OSC_Res = [10,10]
        self._OSC_Divice_Connecter_Pos = [0.5,0.75]
        self.OSC_Communicator = OSC_Backend()
        self.Update_Vars = []
        
        

    def Draw(self, Width, Height):

        if not self._OSC_Res[0] == Width or not self._OSC_Res[1] == Height:
            self._OSC_New_Draw = True
            self._OSC_Res = [Width,Height]

        if self._OSC_New_Draw:
            
            self._OSCGUI_Surface = pygame.Surface((Width, Height))

            self._OSCGUI_Surface.fill((60,60,60)) # filling this pannel

            # Toggle Background Shape (rect)

            self._OSC_Toggle_Rect = [Width*self._OSC_Toggle_Pos_Ratio[0],Height*self._OSC_Toggle_Pos_Ratio[1],
                        (1-(self._OSC_Toggle_Pos_Ratio[0]+self._OSC_Toggle_Pos_Ratio[0]))*Width,Height*self._OSC_Toggle_Pos_Ratio[2]] # Gross position of this shape



            # Begin the indicator Code

            Indicator_Center_Height = (Height*(self._OSC_Toggle_Pos_Ratio[2]/2))+(Height*self._OSC_Toggle_Pos_Ratio[1])

            IndicatorRadius = (Height*self._OSC_Toggle_Pos_Ratio[2])/2

            IndicatorPos = [(Width*self._OSC_Toggle_Pos_Ratio[0])+IndicatorRadius,
                        ((Width*self._OSC_Toggle_Pos_Ratio[0])+(1-(self._OSC_Toggle_Pos_Ratio[0]+self._OSC_Toggle_Pos_Ratio[0]))*Width)-IndicatorRadius]

            try:
                Indicator_Animation_Status = (self._OSC_Switch_Animation_Speed-self._OSC_Switch_Animation_Value)/self._OSC_Switch_Animation_Speed
            except:
                Indicator_Animation_Status = 0

            if self._OSC_Switch_Animation_Value > 0:
                self._OSC_Switch_Animation_Value -= 1
            else:
                self._OSC_New_Draw = False

            self._OSC_Indicator_Colors

            Green = _smooth_value_list(Indicator_Animation_Status,[10,255],self._OSC_Toggle)
            Red = _smooth_value_list(Indicator_Animation_Status,[255,10],self._OSC_Toggle)

            # End indicator code?

            # Start The Connection Indicator Drawing Code

            Div_Con_Ind_Pos_Coord = [self._OSC_Divice_Connecter_Pos[0]*Width,self._OSC_Divice_Connecter_Pos[1]*Height]

            Div_Con_Ind_Color = [0,0,0]
            
            try:
                if self.OSC_Communicator.Device.Connected:
                    Div_Con_Ind_Color = [29,255,29]
                elif self.OSC_Communicator.Searching:
                    Div_Con_Ind_Color = [255,215,0]
                else:
                    Div_Con_Ind_Color = [255,20,20]
            except:
                pass

            pygame.draw.rect(self._OSCGUI_Surface, (120,120,120), self._OSC_Toggle_Rect) # Draw the switch base thing
            pygame.draw.circle(self._OSCGUI_Surface, [Red,Green,10], (_smooth_value_list(Indicator_Animation_Status,IndicatorPos,self._OSC_Toggle), Indicator_Center_Height), IndicatorRadius, 0)
            pygame.draw.circle(self._OSCGUI_Surface, Div_Con_Ind_Color, Div_Con_Ind_Pos_Coord, IndicatorRadius*0.8, 0)

        return self._OSCGUI_Surface

                
                

    def Update(self, Mouse, Keyboard = []):

        if Mouse.Pressed[0]:
            
            if _detect_in_rect(Mouse.Pos, self._OSC_Toggle_Rect):
                
                self._OSC_Toggle = not self._OSC_Toggle

                self._OSC_Switch_Animation_Value = self._OSC_Switch_Animation_Speed

                self._OSC_New_Draw = True

                self.OSC_Communicator.Connect_To_Device = self._OSC_Toggle

        Update_List = [self.OSC_Communicator.Device.Connected, self.OSC_Communicator.Searching]

        if not self.Update_Vars == Update_List:
            self.Update_Vars = Update_List
            self._OSC_New_Draw = True

                
            


        




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

        Mouse.Update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())

        
        screen.blit(OSC_Module.Draw(width, height),[0,0])
        
        OSC_Module.Update(Mouse)

       


        # flip display and clock tick
        pygame.display.flip()
        clock.tick(FPS)


