import collections
import typing
from .message import HttpMessage

# Global Variables
__all__ = [
    "HttpResponse"
]


class HttpResponse(HttpMessage):
    def __init__(self, headers: typing.Iterable[typing.Tuple[bytes, bytes]]=None):
        HttpMessage.__init__(self)
        if headers is not None:
            for key, val in headers:
                self.headers[key] = val
        self.status_code = 0
        self.status = b''

    def on_status(self, status: bytes):
        self.status = status

    def to_bytes(self) -> bytes:
        parts = [b'HTTP/%b %d %b' % (self.version, self.status_code, self.status)]
        if len(self.headers) > 0:
            parts.append(self.headers.to_bytes())
        if len(self.cookies) > 0 and self.cookies.is_changed():
            parts.append(self.cookies.to_bytes(set_cookie=True))
        parts.append(b'')
        parts.append(self.body)
        return b'\r\n'.join(parts)
