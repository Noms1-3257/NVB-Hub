import pygame

class Sprite:

    def __init__(self):

        self.Images = []

        self.Sprite = 0

        self.Draw_Update_Vars = []

        self.Pos = [0,0]

        self.Size = [0,0]

        self.Surface = None

    def Load_Images(self, Paths):

        if type(Paths) == str:

            self.Images.append(pygame.image.load(Paths))

            return

        if type(Paths) == list:

            for path in Paths:

                self.Images.append(pygame.image.load(path))

            return
            

    def Draw(self, Width, Height, Pos = None, Size = None):

        if Pos == None:
            Pos = self.Pos
        if Size == None:
            Size = self.Size

        Draw_Update_Vars = [Width, Height, Pos , Size]

        if not self.Draw_Update_Vars == Draw_Update_Vars:

            self.Surface = pygame.Surface.convert_alpha( pygame.Surface((Width, Height)) )

            self.Surface.fill((0,0,0,0))

            Thing_To_Blit = pygame.transform.scale(self.Images[self.Sprite], [Width*Size[0],Height*Size[1]])

            self.Surface.blit(Thing_To_Blit, [Width*Pos[0],Height*Pos[1]])

        return self.Surface

        


if __name__ == "__main__":
    
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = 30

    Image_Root = "./tmp/"

    pygame.display.set_caption("Animation_Test")

    # ini the sprite

    Sprite_Test = Sprite()

    Sprite_Images = [Image_Root+"OSC_Off.png", Image_Root+"OSC_Searching.png", Image_Root+"OSC_Connected.png"]

    Sprite_Test.Load_Images(Sprite_Images)

    Sprite_Test.Sprite = 2

    #images loaded

    while True:


        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)


        
        screen.fill((100,60,60))
        screen.blit(Sprite_Test.Draw(width, height, [0.25,0.25], [0.4,0.25]),[0,0])
        # pygame.mouse.get_pos()  pygame.mouse.get_pressed()
        


        pygame.display.flip()
        clock.tick(FPS)
                    
