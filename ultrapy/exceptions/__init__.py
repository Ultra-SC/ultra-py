class UnhandledError(Exception):
    def __init__(self, message="Unknown error"):
        super().__init__(message)


class WsConnectionError(Exception):
    def __init__(self, message="Unknown WebSocket connection error"):
        super().__init__(message)


class UploadError(Exception):
    def __init__(self, message="Unknown upload error"):
        super().__init__(message)
