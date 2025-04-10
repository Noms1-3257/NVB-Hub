import pygame


# Data Objects For Inputs
class _Button:
    def __init__(self, Pos = [0,0], Size = [20,10], Name = "Button", Indicator_Ratio = 0.1, On_Color = [5,244,5], Off_Color = [244,5,5], Back_Color = [90,90,90], Ratio_Driven_Position = False):
        self.Pos = Pos
        self.Size = Size
        self.Name = Name
        self.Value = False
        self.On_Color = On_Color
        self.Off_Color = Off_Color
        self.Back_Color = Back_Color
        self.Indicator_Ratio = Indicator_Ratio
        self.Ratio_Driven_Position = Ratio_Driven_Position
        self.Visual_rect = [0,0,1,1]

    def Toggle(self):
        self.Value = not self.Value

    def Color(self):
        if self.Value:
            return self.On_Color
        else:
            return self.Off_Color

    def Draw(self, Width, Height):

        if self.Ratio_Driven_Position:
            Pos = [Width*self.Pos[0], Height*self.Pos[1]]
            
            Size = [min(Width, Height) * self.Size[0], min(Width, Height)* self.Size[1]]

            BackGround_Rect = [Pos[0] ,Pos[1] ,Size[0] ,Size[1]]

            Ind_Scale = [Size[0] * self.Indicator_Ratio, Size[1] * self.Indicator_Ratio]
            
            Indicator_Rect = [Pos[0] + Ind_Scale[0] ,Pos[1] + Ind_Scale[1] ,Size[0] - (Ind_Scale[0]*2),Size[1] - (Ind_Scale[1]*2)]

            self.Visual_rect = BackGround_Rect

            return BackGround_Rect, Indicator_Rect

        else:

            BackGround_Rect = [self.Pos[0] ,self.Pos[1] ,self.Size[0] ,self.Size[1]]

            Ind_Scale = [self.Size[0] * self.Indicator_Ratio, self.Size[1] * self.Indicator_Ratio]

            Indicator_Rect = [self.Pos[0] + Ind_Scale[0] ,self.Pos[1] + Ind_Scale[1] ,self.Size[0] - (Ind_Scale[0]*2),self.Size[1] - (Ind_Scale[1]*2)]

            self.Visual_rect = BackGround_Rect

            return BackGround_Rect, Indicator_Rect

        
        

class _Slider:
    def __init__(self, Pos = [0,0], Size = [20,10], Name = "Slider", Ratio_Driven_Position = False, Vertical = False, Indicator_Color = [255,100,50], Background_Color = [90,90,90]):
        self.Pos = Pos
        self.Size = Size
        self.Name = Name
        self.Value = 0
        self.Visual_rect = [0,0,1,1]
        self.Ratio_Driven_Position = Ratio_Driven_Position
        self.Vertical = Vertical

        self.Indicator_Color = Indicator_Color
        self.Background_Color = Background_Color

    def Draw(self, Width, Height):

        if self.Ratio_Driven_Position:

            Pos = [Width*self.Pos[0], Height*self.Pos[1]]
            
            Size = [min(Width, Height) * self.Size[0], min(Width, Height)* self.Size[1]]

            BackGround_Rect = [Pos[0] ,Pos[1] ,Size[0] ,Size[1]]

            self.Visual_rect = BackGround_Rect

            Indicator_Size = min(Size[0] ,Size[1])/2

            if not self.Vertical:

                Indicator_Y = Pos[1] + (Size[1]/2)

                Indicator_X = Pos[0] + (BackGround_Rect[2]*self.Value)

                return BackGround_Rect, [Indicator_X,Indicator_Y], Indicator_Size

    def Change_On_Mouse(self, Mouse):

        MouseX = Mouse.Pos[0]

        Slider_Min = self.Visual_rect[0]
        Slider_Max = Slider_Min+self.Visual_rect[2]

        if MouseX < Slider_Min:

            self.Value = 0

        elif MouseX > Slider_Max:

            self.Value = 1

        else:
            self.Value = (MouseX-Slider_Min)/(Slider_Max-Slider_Min)

                

                

            

            




#helper functions for inputs

def Check_Mouse_In_Visual(Mouse, Object):
    Mouse_Pos = Mouse.Pos

    
    Button_U = Object.Visual_rect[1]
    Button_D = Button_U+Object.Visual_rect[3]
    Button_L = Object.Visual_rect[0]
    Button_R = Button_L+Object.Visual_rect[2]
    

    if Mouse_Pos[1] > Button_U and Mouse_Pos[1] < Button_D:
        
        if Mouse_Pos[0] > Button_L and Mouse_Pos[0] < Button_R:

            return True

    return False
    

#Actual input handler and builder
class Inputs:
    def __init__(self):
        self.Sliders = []
        self.Buttons = []

        self.Sellected = None

        self.Update_Vars = []

        self.Surface = None
        self.Surface_Update = True
        self.Fresh_Draw = True

    def Update(self, Mouse): # main update for stuff

        if Mouse.Pressed[0]:
            
            if not self.Sellected:
                
                for Button in self.Buttons:
                    
                    if Check_Mouse_In_Visual(Mouse, Button):
                        
                        Button.Toggle()

                        self.Surface_Update = True

                for Slider in self.Sliders:

                    if Check_Mouse_In_Visual(Mouse, Slider):

                        self.Sellected = Slider

                        self.Surface_Update = True

        if Mouse.Held[0] and self.Sellected:

            self.Sellected.Change_On_Mouse(Mouse)

            self.Surface_Update = True

        elif not Mouse.Held[0] and self.Sellected:

            self.Sellected = None

                        

            

        

            
            

    def Draw(self, Width, Height): # Draw everything to a surface

        self.Fresh_Draw = False # This is for info for other scripts

        Update_Vars = [Width, Height]

        if not self.Update_Vars == Update_Vars:
            self.Surface_Update = True
            self.Update_Vars = Update_Vars
            self.Surface = pygame.Surface((Width, Height)) # set surface
        
            

        

        if self.Surface_Update: # If so we need to redraw everything

            self.Fresh_Draw = True

            

            # Do not fill, this is just a overlay

        
            for Button in self.Buttons: # Button Drawing to Surface
                #Draw Button Backing
                Background, Indicator = Button.Draw(Width, Height)

                pygame.draw.rect(self.Surface, Button.Back_Color, Background)
                pygame.draw.rect(self.Surface, Button.Color(), Indicator)

            for Slider in self.Sliders:

                rect, ind_pos, ind_size = Slider.Draw(Width, Height)

                pygame.draw.rect(self.Surface, Slider.Background_Color, rect)

                pygame.draw.circle(self.Surface, Slider.Background_Color, [rect[0],ind_pos[1]], ind_size, 0)

                pygame.draw.circle(self.Surface, Slider.Background_Color, [rect[0]+rect[2],ind_pos[1]], ind_size, 0)
                
                pygame.draw.circle(self.Surface, Slider.Indicator_Color, ind_pos, ind_size, 0)

            


            
        self.Surface_Update = False
        self.Surface.set_colorkey((0, 0, 0)) 
        return self.Surface


    def Create_Slider(self, Pos = [0,0], Size = [20,10], Name = "Slider", Ratio_Driven_Position = False, Vertical = False):
        New_Slider = _Slider(Pos, Size, Name, Ratio_Driven_Position = Ratio_Driven_Position, Vertical = Vertical)
        self.Sliders.append(New_Slider)
        return New_Slider

    def Create_Button(self, Pos = [0,0], Size = [20,10], Name = "Button", Ratio_Driven_Position = False):
        New_Button = _Button(Pos, Size, Name, Ratio_Driven_Position = Ratio_Driven_Position)
        self.Buttons.append(New_Button)
        return New_Button

    
        

        
if __name__ == "__main__":
    from mouse_iterator import Mouse_Iterator
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30

    pygame.display.set_caption("Manual")

    Mouse = Mouse_Iterator()
    Module_Inputs = Inputs()

    #Button = Module_Inputs.Create_Button([50,50], [50,50], Ratio_Driven_Position = False)
    Button = Module_Inputs.Create_Button([0.25,0.25], [0.1,0.1], Ratio_Driven_Position = True)
    Slider = Module_Inputs.Create_Slider([0.3,0.5], [0.25,0.05], Ratio_Driven_Position = True)


    while True:

        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)


        Mouse.Update(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
        Module_Inputs.Update(Mouse)
        screen.blit(Module_Inputs.Draw(width, height),[0,0])
        # pygame.mouse.get_pos()  pygame.mouse.get_pressed()
        


        pygame.display.flip()
        clock.tick(FPS)



