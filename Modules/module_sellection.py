import pygame

class _Module:
    def __init__(self, Name, Class):
        self.Name = Name
        self.Class = Class

class Module:

    def __init__(self):

        #The Manual One
        from Modules.manualv2 import Module as MANUALV2_MODULE
        from Modules.vrc_orph_module import Module as VRC_ORPH_MODULE
        from Modules.vrc_pen_module import Module as VRC_PEN_MODULE
        from Modules.RmCt.RmCt_Module import Module as RMCT_MODULE
        ManualV2_Module = _Module("Manual",MANUALV2_MODULE())
        vrc_Orph_Module = _Module("VRChat Orph", VRC_ORPH_MODULE())
        vrc_Pen_Module = _Module("VRChat Pen", VRC_PEN_MODULE())
        rmct_module = _Module("RmCt", RMCT_MODULE())


        #Add more
        
        
        self.Modules = [ManualV2_Module, vrc_Orph_Module, vrc_Pen_Module, rmct_module]
        self.Selected = None
        self.Update_Vars = []
        self.Background_Color = [50,50,50]
        self.Text_Color = [200,200,200]
        self.Text_Dist_From_Edge = 0.15
        self.Text_Scale_Value = 0.15
        self.Surface = None


        self.Back_Surface = pygame.image.load('./Modules/Assets/Back.png')
        self.Back_Ratio = 0.1

    def Draw(self, Width, Height):

        
        
        if self.Selected:
            Sellected_Surface = self.Selected.Class.Draw(Width, Height)
            Back_Scale = min(Width, Height)*self.Back_Ratio
            Back_Scale = [Back_Scale,Back_Scale]

            

            Sellected_Surface.blit(pygame.transform.scale(self.Back_Surface, Back_Scale), [0,0])
            return Sellected_Surface
        else:

            Update_Vars = [Width, Height]

            if not Update_Vars == self.Update_Vars:

                Surface = pygame.Surface((Width, Height))

                Surface.fill(self.Background_Color)                

                self.Update_Vars = Update_Vars
            
                Module_Offset = Height/len(self.Modules)
                
                Text_Font = pygame.font.Font(None, round(min(Height,Width)*self.Text_Scale_Value))
            
                i=0
                for ListModule in self.Modules:
                    Text_Y_Pos = (Module_Offset*i)+(Module_Offset/2)
                    Line_Y_Pos = Module_Offset*i
                    
                    Text_Surface = Text_Font.render(ListModule.Name, True, self.Text_Color)
                    
                    Surface.blit(Text_Surface, [self.Text_Dist_From_Edge*Width, Text_Y_Pos])
                    
                    pygame.draw.line(Surface, (200,30,20), (0,Line_Y_Pos),(Width,Line_Y_Pos),3)
                    
                    i+=1

                Text_Surface = Text_Font.render("Sellect Module", True, self.Text_Color)
                Surface.blit(Text_Surface, [0, 0])

                self.Surface = Surface
                
            return self.Surface
                    
                
            
            
        
            

    def Update(self, Mouse, Keyboard):

        if self.Selected:

            if Mouse.Pressed[0]:
                if Mouse.Pos[0] < (self.Update_Vars[0]*self.Back_Ratio) and Mouse.Pos[1] < (self.Update_Vars[1]*self.Back_Ratio):
                    self.Selected = None
                    return

            self.Selected.Class.Update(Mouse, Keyboard)

        else:

            if Mouse.Pressed[0] and Mouse.Pos[0] > 0:

                Module_Offset = self.Update_Vars[1]/len(self.Modules)

                i=0
                for ListModule in self.Modules:
                    Bottom = Module_Offset*i
                    Top = Module_Offset*(1+i)

                    if Mouse.Pos[1] > Bottom and Mouse.Pos[1] < Top:
                        self.Selected = ListModule
                        return
                    i+=1

                

                




    
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
