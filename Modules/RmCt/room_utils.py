import asyncio
import websockets
import json
import threading

def _Packet_Parser(Data):
    return json.loads(Data)


class Room:
    # init function
    def __init__(self):
        self.ip = "localhost"
        self.port = "8705"

        self.Values = [0]

        self.RoomCode = "None"

        self.Run = False

        self.Websocket = None

    # start the webserver loop and connect to server
    def start(self):
        self.Run = True
        UpdateLoop = threading.Thread(target=self.StartRoomLoop)
        UpdateLoop.daemon = True
        UpdateLoop.start()
        
        

    # stop the webserver to reduce server load
    def stop(self):
        self.Run = False

    # Function to create and init the room
    async def _CreateRoom(self):

        Packet = '{"Type":"NewRoom"}'

        await self.Websocket.send(Packet) # send request to make a room


    

    # Start the thread and stuff
    def StartRoomLoop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.RoomServer())
        

    async def PacketHandler(self, Packet):
        
        if Packet["Type"] == "UpdateRoomValue":

            self.Values[Packet["Number"]] = Packet["Data"]

        if Packet["Type"] == "RoomCodeReturn":

            self.RoomCode = Packet["Data"]
        

    
    # this is the main server loop
    async def RoomServer(self):
        
        uri = f"ws://{self.ip}:{self.port}"
        
        async with websockets.connect(uri) as websocket:
            # set the websocket refrence
            self.Websocket = websocket

            await self._CreateRoom()

            while self.Run:
                try:
                    responce = await asyncio.wait_for(websocket.recv(), timeout=0.1)

                    await self.PacketHandler(_Packet_Parser(responce))
                    print(responce)
                except:
                    response = ""
                

            

            

            # now we connected, lets do all that shite and init the connection
            # as a room cause yes

if __name__ == "__main__":
    TestRoom = Room()
    TestRoom.start()

    # do more logic here for the main app

    
