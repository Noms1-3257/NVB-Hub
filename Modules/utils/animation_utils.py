import pygame
try:
    from timer import Timer
except:
    from utils.timer import Timer

class _Frame:
    def __init__(self, Pos, Size, Color, Time):
        self.Pos = Pos
        self.Size = Size
        self.Color = Color
        self.Time = Time

def _List_Multiply(List, Mult):
    New = []
    for x in List:
        New.append(x*Mult)

    return New

def _List_Add(List1, List2):
    New = []
    i=0
    for x in List1:
        New.append(x+List2[i])
        i+=1
    return New

class _Anim_Circle:
    def __init__(self, Ratio_Mode = True):
        self.Frames = []
        self.Ratio_Mode = Ratio_Mode
        self.Type = "Circle"
        self.Over = True
        self.Last_Return = []

    def _Frame_Tween(self, Frame1, Frame2, Ratio ,Reverse):
        if Reverse:
            Frame_1_Mult = Ratio
            Frame_2_Mult = 1-Ratio
        else:
            Frame_1_Mult = 1-Ratio
            Frame_2_Mult = Ratio


        Frame_1_Pos = _List_Multiply(Frame1.Pos, Frame_1_Mult)
        Frame_1_Size = Frame1.Size * Frame_1_Mult
        Frame_1_Color = _List_Multiply(Frame1.Color, Frame_1_Mult)

        Frame_2_Pos = _List_Multiply(Frame2.Pos, Frame_2_Mult)
        Frame_2_Size = Frame2.Size * Frame_2_Mult
        Frame_2_Color = _List_Multiply(Frame2.Color, Frame_2_Mult)

        Pos = _List_Add(Frame_1_Pos, Frame_2_Pos)
        Size = Frame_1_Size + Frame_2_Size
        Color = _List_Add(Frame_1_Color, Frame_2_Color)

        self.Last_Return = [Pos, Size, Color]

        return Pos, Size, Color

    def Add_Frame(self, Pos, Size, Color, Time):
        self.Frames.append(_Frame(Pos, Size, Color, Time))

    def Evaluate_From_Time(self, Time, Reverse):
        
        if self.Over and not self.Last_Return == []:
            return self.Last_Return[0], self.Last_Return[1], self.Last_Return[2]


        
        if len(self.Frames) == 0:
            return [0,0], 10, [255,0,0]

        Frame_Pre = None
        Frame_Post = None
        # I am only using this for 2 frame states, so I will remain lazy

        # The commented out code needs fixing n shit

        
        Frame_Pre = self.Frames[0]
        Frame_Post = self.Frames[1]


        
        '''
        i=0
        for Frame in self.Frames:
            if Frame.Time > Time:
                Frame_Post = Frame
                
                break
            Frame_Pre = Frame
            i+=1

        if i == 0:
            
            Frame_Pre = Frame_Post

        if Frame_Post == None:
            Frame_Post = Frame_Pre
            self.Over = True '''

        try:
            Frame_Ratio = (Time-Frame_Pre.Time)/(Frame_Post.Time-Frame_Pre.Time)
        except:
            
            Frame_Ratio = int(Reverse)

        Frame_Ratio = min(Frame_Ratio,1)
        Frame_Ratio = max(Frame_Ratio,0)

        if Frame_Ratio >= 1:
            self.Over = True

        return self._Frame_Tween(Frame_Pre, Frame_Post, Frame_Ratio, Reverse) # This reverse here is just a hack for 2 frame animations


        


class Animator:
    def __init__(self):
        self.Objects = []
        self.Play = False
        self.State = False
        self.Reverse = False
        self.Timer = Timer()

        self.Surface = None

    def Play_Animation(self, Reverse = False):
        self.Play = True
        self.Reverse = Reverse
        self.Timer.reset()
        self.Timer.start()

        for Obj in self.Objects:
            Obj.Over = False

    
        

    def Create_Circle(self):
        Anim = _Anim_Circle()
        self.Objects.append(Anim)
        return Anim
        

    def Draw(self, Width, Height, Update = False):

        

        if self.Play or self.Surface == None or Update:
            Play_Checker = True

            self.Surface = pygame.Surface.convert_alpha( pygame.Surface((Width, Height)) )

            Cur_Time = self.Timer.get_current_time()

            for Obj in self.Objects:
                
                if Obj.Over:
                    Play_Checker = False

                if Obj.Type == "Circle":

                    Pos, Size, Color = Obj.Evaluate_From_Time(Cur_Time, self.Reverse)

                    if Obj.Ratio_Mode:
                        Pos = [Pos[0]*Width, Pos[1]*Height]

                    pygame.draw.circle(self.Surface, Color, Pos, Size*Height, 0)


            self.Play = Play_Checker
            self.Surface.set_colorkey((0, 0, 0))

        

        return self.Surface


            
if __name__ == "__main__":
    
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30

    pygame.display.set_caption("Animation_Test")

    #Setup Animator

    Animation = Animator()

    Toggle_Head = Animation.Create_Circle()

    Toggle_Head.Add_Frame([0,0], 0.1, [255,0,0], 0)
    Toggle_Head.Add_Frame([1,1], 0.1, [0,255,0], 10)

    Animation_Permlock = True

    Animation.Play_Animation()

    

    

    while True:
        Update_Screen = False

        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                Update_Screen = True
                
        if Animation_Permlock and not Animation.Play:
            Animation.Play_Animation(Reverse = True)
            Animation_Permlock = False

        
        screen.fill((100,60,60))
        screen.blit(Animation.Draw(width, height, Update_Screen),[0,0])
        # pygame.mouse.get_pos()  pygame.mouse.get_pressed()
        


        pygame.display.flip()
        clock.tick(FPS)
                    

                    

                    
            
