from uuid import uuid4
from .protocol import package as pkg
from threading import Event
import asyncio
import json
import websockets

class Device():
    """
    Open an connection to the websocket server.

    (send): Will send a package to the server and wait for an answer.
    (close): Will close the connection to the server.

    Can be used as a context manager.

    """
    def __init__(self, uri, loop=None):
        self._id = uuid4().hex
        self.uri = uri
        self.stopped = Event()
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.reconnections = 0
        self.reconnect_limit = 3

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.websocket.close()

    def close(self):
        self.stopped.set()
    
    async def connect(self):
        """
        Connect to the websocket server.
        """
        self.websocket = await websockets.connect(self.uri)
    
    async def reconnect(self):
        """
        Reconnect to the websocket server.
        """
        if self.reconnections < self.reconnect_limit:   # Avoid infinite loop
            self.reconnections += 1                     # Increase reconnection counter
            try:                                        # Try to reconnect
                await self.connect()                    # Connect to the websocket server
                self.reconnections = 0                  # Reset reconnection counter
            except ConnectionRefusedError:              # If connection is refused
                import random
                await asyncio.sleep(random.random())    # Wait 0.N second
                await self.reconnect()                  # Try to reconnect again
        else:                                           # If reconnection limit is reached
            self.close()                                # Close the connection
            raise ConnectionError("Connection to server lost.")
        

    async def send(self, package):
        """
        Send a package to the server and wait for an answer.
        (package): protocol.package object
        """
        try:
            if not isinstance(package, pkg):
                raise TypeError(f"package must be instance of {pkg}")
            await self.websocket.send(json.dumps(package.json()))
            if package.read:
                return pkg(**json.loads(await self.websocket.recv()))
        except websockets.exceptions.ConnectionClosed:
            await self.reconnect()
            await self.send(package)


async def unit_test(show=False):
    """
    unit test for the client
    (show): if True will print the package sent and received

    Steps:
        1. Connect to the server
        2. Send a 'n' random packages
        3. Check integrity of the packages
        4. Close the connection
    """

    value = False
    show and print('='*20, 'UNIT TEST', '='*20)
    show and print("[Starting] Unit Test - MarlinAPI Websocket Client")
    try:
        from .protocol import example_packages
        test_packages = example_packages(10)

        async with Device("ws://192.168.4.1:8010") as X:
            assert X.websocket.open, "Websocket is not open"
            show and print("MarlinAPI-Client open --- OK")

            commands = [await X.send(pk) for pk in test_packages]
            assert commands is not None, 'No commands received, check if marlin is connected on server'
            show and print('Commands send/received --- OK' )

            for get, post in zip(commands, test_packages):
                if get is not None:
                    assert get.data[0] == post._id, 'received package data not match with correspondent send package id, serial should be hard reseted'
            show and print('Commands data match --- OK' )

        assert X.websocket.closed, 'Websocket is not closed, check __aexit__ method'
        show and print('MarlinAPI-Client closed --- OK' )
        value = True
    except ConnectionRefusedError:
        show and print("MarlinAPI-Client open --- Failed")
    finally:
        show and print("[Finished] Unit Test - MarlinAPI Websocket Client")
        show and print('='*51)
        return value

async def main(uri, raw=False):
    """
    Connect to the server and wait for user input data.
    (uri): Websocket server uri
    (raw->False): Don't convert data to package object. 
    """
    async with Device(uri) as c:
        try:
            while c.websocket.open:
                data = input('Send: ')
                if raw:
                    await c.send(data)
                else:
                    qtd_ansers = int(input('Qtd answers: '))
                    timeout = int(input('Timeout: '))
                    echo = input('Last response: ') if qtd_ansers <0 else "ok"
                    print("Echo :", await c.send(pkg(data=data, answer_lines=qtd_ansers, timeout=timeout, end_echo=echo)))
        except KeyboardInterrupt:
            c.close()

if __name__ == "__main__":
    asyncio.run(main("ws:0.0.0.0:8010"))
