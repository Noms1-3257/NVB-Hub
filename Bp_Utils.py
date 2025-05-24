import asyncio, threading
from bleak import BleakClient, BleakScanner

# Nordic UART Service (NUS) UUIDs
NUS_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
NUS_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Characteristic for writing to the device
NUS_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Characteristic for notifications from the device





class Device:
    def __init__(self):
        self.Send_Buffer = []
        self.Recieve_Buffer = []
        self.Connected = False
        self.Api_Version = "None"

    

    def Send(self, data):
        self.Send_Buffer.append(data)

    def Recieve(self):
        TMP = self.Recieve_Buffer
        self.Recieve_Buffer = []
        return TMP


    

    def Connect(self, Name=None, Name_Prefix = "NVB", Search_Length = 10):
        
        device = asyncio.run(self._discover_device(Name, Name_Prefix, Search_Length = Search_Length))
        #Gross hack time baby!

        def ConnHandle():
            asyncio.run(self._Connection_Handler(device))
        
        if device:
            
            self.Connected = True
            threading.Thread(target=ConnHandle).start()
        else:
            return False

    def Disconnect(self):
        
        self.Connected = False
        

        
        

    def _Notification_Handler(self, sender, data):
        data = data.decode('utf-8')
        self.Recieve_Buffer.append(data)
        
    async def _discover_device(self, Name=None, Name_Prefix = "NVB", Search_Length = 10):
        devices = await BleakScanner.discover(Search_Length)
        device = None
        for d in devices:
           
            if Name:
                
                if d.name == TARGET_NAME:
                    device = d
                    break
            else:
                try:
                    if d.name.startswith(Name_Prefix):
                        if d.name == "NVB0" or d.name == "NVB1":
                            self.Api_Version = "V1"
                        
                        device = d
                        break
                except:
                    pass

        if not device:
            return False
        else:
            return device


    async def _Connection_Handler(self, device):
        

        
        async with BleakClient(device, timeout = 10) as client:
            
            await client.start_notify(NUS_TX_CHAR_UUID, self._Notification_Handler)
            self.Connected = True
            while True:
                if not self.Connected:
                    kill_data = "0,0|"
                    await client.write_gatt_char(NUS_RX_CHAR_UUID, kill_data.encode("utf-8"))
                    break
                
                if not client.is_connected:
                    self.Connected = False
                    break
                try:
                    if len(self.Send_Buffer) > 0:
                        data = self.Send_Buffer[::-1][0]
                        print("[Bp_Utils] - Sending {data}")
                        await client.write_gatt_char(NUS_RX_CHAR_UUID, data.encode("utf-8"))
                        for data in self.Send_Buffer:
                            del self.Send_Buffer[0]
                    await asyncio.sleep(0.01)
                except:
                    self.Connected = False
                    break
                    
        
            #print("Connection Attempt Failed")
            #self.Connected = False
            

