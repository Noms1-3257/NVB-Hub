import pygame
import sys
import threading
from mouse_iterator import Mouse_Iterator
from keyboard_iterator import Keyboard_Iterator
import OSC_ModuleV2_MP as OSC_Module





#Hacky test Go brrrr
'''
from Modules.bp_manual import Module

Manual_Module = Module()
'''
#End hacky test






class _App:
    def __init__(self):
        self.Running = True
        self.Base_Color = [30,30,30]
        self.FPS = 45
        self.Window_Size = [30,30]
        self.Mouse = Mouse_Iterator()
        self.Keyboard = Keyboard_Iterator()
        self.OSC_Module = OSC_Module.Module()
        

if __name__ == "__main__":


    


    
    # Pygame Stuff Init
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()



    #Import Crappy Module Sellection
    from Modules.module_sellection import Module
    Module_Sellector = Module()

    # app appearance
    icon = pygame.image.load("./app.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("NVB HUB")

    
    App = _App()
    App.OSC_Module._Init_And_Start_Worker()
    App.Window_Size = [width, height]

    # Main Loop
    while App.Running:

        
        screen.fill(App.Base_Color) 
        for event in pygame.event.get(): # Basic pygame events, quitting and resize
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                App.Window_Size = [width, height]
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            if event.type == pygame.QUIT: # End Quit Routine
                App.Running = False

        #OSC MODULE
        App.OSC_Module.Update(App.Mouse, App.Keyboard)
        screen.blit(App.OSC_Module.Draw(width/2, height),[0,0])
        #END OSC MODULE
        App.Mouse.Pos = [App.Mouse.Pos[0]-(width/2),App.Mouse.Pos[1]] # Hack The Mouse Pos To Be For Modules

        '''
        #START JANK MANUAL
        Manual_Module.Update(App.Mouse)
        screen.blit(Manual_Module.Draw(width/2, height),[width/2,0])
        #End Jank Manual
        '''
        
        #Start Module Sellection
        Module_Sellector.Update(App.Mouse, App.Keyboard)
        screen.blit(Module_Sellector.Draw(width/2, height),[width/2,0])
        #End Module Sellection

        App.Mouse.Update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(App.FPS)

    pygame.quit()
    App.OSC_Module._Stop()
