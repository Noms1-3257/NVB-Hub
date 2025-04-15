from pythonosc import osc_server
import socket
import threading
import time
import copy
from Bp_Utils import Device

class OSC_Backend:
    def __init__(self):

        self.Connect_To_Device = False

        self.Vibration_Intensity = [0,0] # The Vibration intensity

        self._Cur_Vibration = 0 # The curent vibration

        self.Device = Device()

        self.Searching = False

        self.Kill_Threads = False

        

        
        # Threads for handling things
        self.Device_Thread = threading.Thread(target=self._Device_Handler)
        self.OSC_Thread = threading.Thread(target=self._OSC_Handler)

        self.Device_Thread.daemon = True
        self.OSC_Thread.daemon = True

        self.Device_Thread.start()
        self.OSC_Thread.start()


    def KillBackend(self):
        self.Kill_Threads = True


        

    def _Device_Handler(self):
        
        
        from Bp_Utils import Device # Init device stuff

        self.Device = Device()
        
        while True: # We run this forever cause we expect to deal with devices
            
            if self.Connect_To_Device: # If we are supposed to be connected and sending data

                if self.Device.Connected:

                    self.Searching = False # We already connected
                    
                    if not self._Cur_Vibration == self.Vibration_Intensity:

                        self._Cur_Vibration = self.Vibration_Intensity # Check curent vibration state, dont wanna spam the same thing

                        self.Device.Send(f"{self.Vibration_Intensity[0]},{self.Vibration_Intensity[0]}|")

                        time.sleep(0.01)

                else:  # Else we not be connected, we need to get on that

                    self.Searching = True

                    self.Device.Connect(Search_Length = 3)

                    if self.Device.Connected: # We just connected, make sure it knows what were doing

                        self.Device.Send(f"{self.Vibration_Intensity[0]},{self.Vibration_Intensity[0]}|")

            else: # We dont need to be connected, fuk that

                if self.Device.Connected:

                    self.Device.Disconnect()

                else:

                    self.Searching = False

                    time.sleep(1)

            if self.Kill_Threads: # KILL SIGNIL
                self.Device.Disconnect()
                self.Searching = False
                return

                    

                    

                
    def _OSC_Handler(self):
        

        from pythonosc import dispatcher

        ip = "127.0.0.1"

        port = 8700

        dispatcher = dispatcher.Dispatcher()

        dispatcher.map("/vibrate", self._OSC_Vibrate_Dispatch)

        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

        server.serve_forever()

        

        

    def _OSC_Vibrate_Dispatch(self, address, *args):
        
        self.Vibration_Intensity = args



if __name__ == "__main__":
    Test_Backend = OSC_Backend()

    Test_Backend.Connect_To_Device = True


                    
                
        
