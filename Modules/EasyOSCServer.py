import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import threading

class EasyOSCServer:
    def __init__(self, ip="127.0.0.1", port=5005):
        self._dispatcher = Dispatcher()
        self._ip = ip
        self._port = port
        self._server = None
        self._loop = None
        self._task = None

    def add_handler(self, address, handler):
        self._dispatcher.map(address, handler)

    def start(self):
        # asyncio runs in main thread or a new thread
        if self._loop is not None and self._loop.is_running():
            print("[EasyOSCServer] Server is already running!")
            return

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        coro = self._create_server()
        self._task = self._loop.create_task(coro)
        threading.Thread(target=self._loop.run_forever, daemon=True).start()
        print(f"[EasyOSCServer] AsyncIO server listening on {self._ip}:{self._port}")

    async def _create_server(self):
        server = AsyncIOOSCUDPServer((self._ip, self._port), self._dispatcher, self._loop)
        transport, protocol = await server.create_serve_endpoint()
        self._server = transport
        # This endpoint stays alive as long as the loop runs

    def stop(self):
        if self._server:
            self._server.close()
            print("[EasyOSCServer] Server stopped.")
            self._server = None
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._loop = None

    def is_running(self):
        return self._loop is not None and self._loop.is_running()
