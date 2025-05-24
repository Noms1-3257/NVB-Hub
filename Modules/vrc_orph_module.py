import pygame
from pythonosc import udp_client
import time

try:
    from EasyOSCServer import EasyOSCServer
except:
    from utils.EasyOSCServer import EasyOSCServer
import threading


try:
    from timer import Timer
except:
    from utils.timer import Timer

from  utils.input_utils import Inputs






class _Passthrough:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 9002
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)
        


    def send_message(self, unused_addr, args, *osc_arguments):
        self.client.send_message(unused_addr, args)




class Timed_Speed_Iterator:
    def __init__(self):

        self.Collection_Secconds = 0.2
        self.Collection = []
        self.Top_Speed = 0
        self.Top_Speed_Bleed = 0.03
        self.Bleed_Secs = 1
        self.Last_Bleed_Time = 0
        self.Speed = 0
        self.Value = 0

        
        

    def _Collection_Time(self):
        try:
            Start = self.Collection[0][1]
            End = self.Collection[::-1][0][1]

            return End-Start
        except:
            return 0


    def _Get_Change_From_Collection(self):
        Change = 0
        i=0
        for Object in self.Collection:
            
            if not i <= 0:
                Change += abs(Object[0]-self.Collection[i-1][0])
            i+=1
        return Change
        

        

    def _Limit_Collection(self):
        while self._Collection_Time() > self.Collection_Secconds:
            del self.Collection[0]

    def _Iterate_Bleed(self, Time):

        Bleed_Mult = (Time-self.Last_Bleed_Time)/self.Bleed_Secs

        self.Last_Bleed_Time = Time

        self.Top_Speed = self.Top_Speed * (1-( self.Top_Speed_Bleed * Bleed_Mult ))

        

        

    

    def Iterate(self, Value, Time):
        
        self.Collection.append([Value, Time])

        self._Limit_Collection()

        Change = self._Get_Change_From_Collection()

        if Change > self.Top_Speed:
            
            self.Top_Speed = Change

        self.Speed = Change
        
        if self.Top_Speed <= 0:
            
            self.Value = 0
        else:
            
            self.Value = Change/self.Top_Speed

        if self.Top_Speed > 0:

            self._Iterate_Bleed(Time)

        return self.Value

        

        

        




class Module:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 9001

        self.OSC_Server = EasyOSCServer(self.ip, self.port)
        self.OSC_Server.add_handler("/avatar/parameters/OGB/Orf/*/*", self.Orph_Handler)

        
        self.Toggle = False
        self.Started = False

        # The osc connection handler
        self.Handler_Thread = threading.Thread(target=self.OSC_Vrc_Handler)
        self.Handler_Thread.daemon = True
        self.Handler_Thread.start()

        # The Passthrough For other OSC apps
        #self.Passthrough = _Passthrough()
        #self.OSC_Server.add_handler("/*", self.Passthrough.send_message)

        # Haptic Timer
        self.Timer = Timer()
        self.Timer.start()

        # Orph Haptic Iterator
        self.Orph_Haptic_Iterator = Timed_Speed_Iterator()
        self.Haptics_Limit = 1
        
        

        # Orph Vars
        self.Orph_Is_Penned = False
        self.Orph_Pen_Value = 0

        #Toggle Switch

        self.Inputs = Inputs()

        self.Module_Toggle = self.Inputs.Create_Button([0.25,0.25], [0.5,0.25], Ratio_Driven_Position = True)

        # Visuals update ccars =

        self.Update_Vars = []
        

        


    def Draw(self, Width, Height):

        Update_Vars = [Width, Height]

        if not self.Update_Vars == Update_Vars:

            self.Surface = pygame.Surface((Width, Height))

            self.Surface.fill((60,60,60))

            self.Surface.blit(self.Inputs.Draw(Width, Height),[0,0])

        return self.Surface

        

        

    def Update(self, Mouse, Keyboard):
        
        self.Inputs.Update(Mouse, Keyboard)

        self.Toggle = self.Module_Toggle.Value
        


    def Orph_Handler(self, address, args , *osc_arguments):
        
        

        # Penetration Stuff
        if address.endswith("NewRoot"):
        
            self.Orph_Pen_Value = float(args)
            
        if address.endswith("NewTip") and float(args) >= 0.98:
            #print("start da vibrations here")
            
            self.Orph_Is_Penned = True
            
        if address.endswith("NewTip") and not float(args) >= 0.98:
            
            self.Orph_Is_Penned = False
            
    

    def OSC_Vrc_Handler(self):

        # Prep OSC client for sending to vibrator

        ip = "127.0.0.1"
        port = 8700
        client = udp_client.SimpleUDPClient(ip, port)

        #client.send_message("/vibrate", [self.Slider.Value,self.Slider.Value])

        OSC_Prev_Send = 0

        Stalling_Timer = Timer()
        Stalling_Timer.start()
        Stall_Ready = True
        Stall_Time = 0.5

        while True:

            time.sleep(0.02)

            if self.Toggle:


                if not self.Started:
                
                    self.Timer.reset()

                    self.OSC_Server.start()

                    self.Orph_Haptic_Iterator.Collection = []

                    self.Started = True

                if self.Orph_Is_Penned:

                    self.Orph_Haptic_Iterator.Iterate(self.Orph_Pen_Value, self.Timer.get_current_time())
                    Stalling_Timer.reset()
                    Stall_Ready = True
                else:

                    self.Orph_Haptic_Iterator.Iterate(self.Orph_Pen_Value, self.Timer.get_current_time())

                    if Stalling_Timer.get_current_time() > Stall_Time and Stall_Ready:

                        client.send_message("/vibrate", [0,0])

                        Stall_Ready = False
                        
                if not self.Orph_Haptic_Iterator.Value == OSC_Prev_Send:

                    

                    Value = self.Haptics_Limit * self.Orph_Haptic_Iterator.Value
                    
                    client.send_message("/vibrate", [Value,Value])

                    OSC_Prev_Send = self.Orph_Haptic_Iterator.Value

                

            elif not self.Toggle:

                if self.Started:

                    self.Timer.reset()

                    self.OSC_Server.stop()

                    self.Started = False

                    client.send_message("/vibrate", [0,0])

                

                

                    




    
if __name__ == "__main__":
    import time
    from mouse_iterator import Mouse_Iterator
    Mouse = Mouse_Iterator()
    Vr_Osc_Module = Module()

    
    

    
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

            
        Mouse.Update(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        Vr_Osc_Module.Update(Mouse)
        screen.blit(Vr_Osc_Module.Draw(width, height),[0,0])
        
    
        pygame.display.flip()
        clock.tick(FPS)
