import re
import base64
import requests
import websockets
from typing.io import BinaryIO
from .exceptions import *

ultra_address: str = requests.get("https://pastebin.com/raw/FPzdGWKu").text
ultra_ws: str = f"ws://{requests.get('https://pastebin.com/raw/8S11wyQQ').text}"


class Token:
    def __init__(self, raw: str):
        data = raw.split(".")
        self.id = data[0]
        self.stamp = data[1]
        self.key = data[2]

    def __str__(self):
        return f"{self.id}.{self.stamp}.{self.key}"


class Response:
    def __init__(self, raw: str):
        response = raw.split(":")
        self.status: str = response[0]
        self.token: Token = None
        self.msg: str = None

        self.is_ok = self.status == "ok"
        if self.is_ok:
            self.token: Token = Token(response[1])
        else:
            self.msg = response[1]

    def unwrap(self) -> Token:
        if self.is_ok:
            return self.token
        raise UploadError(message=self.token)

    def as_img(self, static=False) -> str:
        url = f"https://www.{ultra_address}/img?id={self.unwrap().id}"
        if static:
            page = requests.get(url).text
            matches = re.findall(r'data-mfp-src="([\w\S]+)"', page)
            if matches.__len__() > 0:
                if matches[0].startswith("images"):
                    return f"https://www.{ultra_address}/{matches[0]}"
                return matches[0]
            return "NaN"
        return url


class Client:
    def __init__(self, ws_host=ultra_ws, address=ultra_address):
        self.ws_host = ws_host
        self.address = address
        self.ws = None

    def _is_connected(self) -> bool:
        return self.ws is not None

    def _check_connection(self):
        if self.ws is None:
            raise WsConnectionError(message="WebSocket not connected")

    async def connect(self):
        if self._is_connected:
            try:
                self.ws = await websockets.connect(self.ws_host)
            except websockets.ConnectionClosed:
                raise WsConnectionError(message="Could not establish WebSocket connection")
            except Exception as e:
                raise UnhandledError(message=e.__str__())
        else:
            raise WsConnectionError(message="WebSocket is already connected, but tried to connect again")

    async def disconnect(self):
        if self._is_connected:
            await self.ws.close()
            self.ws = None

    @staticmethod
    def _prepare_payload(title: str, description: str) -> bytes:
        return f"{title}\0{description}\0".encode("utf-8")

    async def _send_data(self, payload: str) -> Response:
        await self.ws.send(payload)
        result_raw: str = await self.ws.recv()
        return Response(result_raw)

    async def send_reader(self, title: str, description: str, file_reader: BinaryIO, close=False) -> Response:
        self._check_connection()
        data = file_reader.read()

        if close:
            file_reader.close()

        payload = Client._prepare_payload(title, description) + base64.b64encode(data)
        return await self._send_data(payload)

    async def send_bytes(self, title: str, description: str, file_content: bytes) -> Response:
        self._check_connection()
        payload = Client._prepare_payload(title, description) + base64.b64encode(file_content)
        return await self._send_data(payload)
