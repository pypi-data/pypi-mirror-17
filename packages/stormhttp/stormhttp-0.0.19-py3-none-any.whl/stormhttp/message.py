import brotli
import gzip
import io
import re
import typing
import zlib
from .headers import HttpHeaders
from .cookies import HttpCookies

# Global Variables
__all__ = [
    "HttpMessage"
]
_COOKIE_REGEX = re.compile(b'([^\\s=;]+)(?:=([^=;]+))?(?:;|$)')
_SUPPORTED_ENCODINGS = {b'gzip', b'deflate', b'br', b'identity'}


class HttpMessage:
    def __init__(self):
        self.headers = HttpHeaders()
        self.cookies = HttpCookies()
        self.body = b''
        self.version = b''

        self._body_buffer = []
        self._header_buffer = []
        self._is_header_complete = False
        self._is_complete = False

    def is_complete(self) -> bool:
        return self._is_complete

    def is_header_complete(self) -> bool:
        return self._is_header_complete

    def to_bytes(self) -> bytes:
        raise NotImplementedError("HttpMessage.to_bytes() is not implemented.")

    def set_encoding(self, encoding: bytes, set_headers: bool=True) -> None:
        """
        Sets the encoding of the body to be a certain Content-Encoding.
        Currently the only supported encodings are identity, gzip, delfate, and brotli.
        :param encoding: Encoding to set the body to be.
        :param set_headers: If True, modifies the headers to reflect the change.
        :return: None
        """
        assert encoding in _SUPPORTED_ENCODINGS
        current_encoding = self.headers.get(b'Content-Encoding', [b'identity'])[0]
        if current_encoding == encoding or len(self.body) == 0:
            return  # No-op if the encoding is already correct.

        # Decoding the current encoding.
        if current_encoding != b'identity':
            if current_encoding == b'br':
                self.body = brotli.decompress(self.body)
            elif current_encoding == b'gzip':
                self.body = gzip.GzipFile(fileobj=io.BytesIO(self.body), mode="rb").read()
            elif current_encoding == b'deflate':
                self.body = zlib.decompress(self.body, -zlib.MAX_WBITS)

        # Re-encoding with the desired encoding.
        if encoding != b'identity':
            if encoding == b'br':
                self.body = brotli.compress(self.body)
            elif encoding == b'gzip':
                out = io.BytesIO()
                gzip.GzipFile(fileobj=out, mode="wb").write(self.body)
                self.body = out.getvalue()
            elif encoding == b'deflate':
                deflate = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
                self.body = deflate.compress(self.body) + deflate.flush()

        # Optionally set the headers.
        if set_headers:
            self.headers[b'Content-Length'] = b'%d' % len(self.body)
            self.headers[b'Content-Encoding'] = encoding

    # httptools parser interface

    def on_header(self, key: typing.Optional[bytes], val: typing.Optional[bytes]):
        self._header_buffer.append((key, val))

    def on_headers_complete(self) -> None:
        _headers = {}
        _key_buffer = []
        _val_buffer = []
        _key = None

        for key, val in self._header_buffer:
            if key is not None:
                if _key_buffer is None:
                    _key_buffer = [key]
                    if _key is not None:
                        _headers[_key] = _headers.get(_key, []) + [b''.join(_val_buffer)]
                    _key = None
                else:
                    _key_buffer.append(key)
            if val is not None:
                if _key is None:
                    _key = b''.join(_key_buffer)
                    _key_buffer = None
                    _val_buffer = []
                _val_buffer.append(val)
        if _key is not None:
            _headers[_key] = _headers.get(_key, []) + [b''.join(_val_buffer)]

        self.headers.update(_headers)
        if b'Cookie' in self.headers:
            self.cookies.update({key: val for key, val in _COOKIE_REGEX.findall(b'; '.join(self.headers[b'Cookie']))})
            del self.headers[b'Cookie']

        self._is_header_complete = True

    def on_body(self, body: bytes) -> None:
        self._body_buffer.append(body)

    def on_message_complete(self) -> None:
        self.body = b''.join(self._body_buffer)
        self._is_complete = True
