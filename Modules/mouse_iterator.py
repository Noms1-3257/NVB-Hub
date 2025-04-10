

class Mouse_Iterator:
    def __init__(self):
        self.Pressed = [False, False, False]
        self.Held = [False, False, False]
        self.Pos = [0,0]
        self._Prev = [False,False,False]

    def Update(self, Pressed, Pos):
        
        self.Pos = Pos

        self.Held = Pressed


        self.Pressed[0] = False
        if not self._Prev[0] and Pressed[0]:
            self.Pressed[0] = True

        self.Pressed[1] = False
        if not self._Prev[1] and Pressed[1]:
            self.Pressed[1] = True

        self.Pressed[2] = False
        if not self._Prev[2] and Pressed[2]:
            self.Pressed[2] = True

        self._Prev = Pressed

        
                

        
    
