from aica_api.ws_client import WebsocketAsyncClient
import time

with WebsocketAsyncClient('ws://localhost:5000/conditions', data_callback=lambda data: print(data)) as ws:
    while ws.is_running():
        time.sleep(1)

