import time
from typing import Any

import msgpack
import numpy as np
import websockets.sync.client


class PolicyClient:
    """Simple websocket client for requesting actions from a replay policy server."""

    def __init__(self, host: str, port: int, api_key: str | None = None):
        self._uri = f"ws://{host}:{port}"
        self._api_key = api_key
        self._packer = msgpack.Packer(default=_pack_array)
        self.metadata: dict[str, Any] = {}
        self._ws = self._wait_for_server()

    def _wait_for_server(self):
        while True:
            try:
                headers = (
                    {"Authorization": f"Api-Key {self._api_key}"}
                    if self._api_key
                    else None
                )
                conn = websockets.sync.client.connect(
                    self._uri,
                    compression=None,
                    max_size=None,
                    additional_headers=headers,
                )
                # Server sends metadata first.
                metadata = conn.recv()
                if not isinstance(metadata, str):
                    self.metadata = msgpack.unpackb(metadata, object_hook=_unpack_array)
                return conn
            except ConnectionRefusedError:
                print(f"Waiting for policy server at {self._uri}...")
                time.sleep(2)

    def infer(self, obs: dict[str, Any]) -> dict[str, Any]:
        self._ws.send(self._packer.pack(obs))
        response = self._ws.recv()
        if isinstance(response, str):
            raise RuntimeError(f"Error in policy server response: {response}")
        return msgpack.unpackb(response, object_hook=_unpack_array)

    def close(self) -> None:
        self._ws.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def _pack_array(obj):
    if (isinstance(obj, (np.ndarray, np.generic))) and obj.dtype.kind in (
        "V",
        "O",
        "c",
    ):
        raise ValueError(f"Unsupported dtype: {obj.dtype}")

    if isinstance(obj, np.ndarray):
        return {
            b"__ndarray__": True,
            b"data": obj.tobytes(),
            b"dtype": obj.dtype.str,
            b"shape": obj.shape,
        }

    if isinstance(obj, np.generic):
        return {
            b"__npgeneric__": True,
            b"data": obj.item(),
            b"dtype": obj.dtype.str,
        }

    return obj


def _unpack_array(obj):
    if b"__ndarray__" in obj:
        return np.ndarray(
            buffer=obj[b"data"],
            dtype=np.dtype(obj[b"dtype"]),
            shape=obj[b"shape"],
        )

    if b"__npgeneric__" in obj:
        return np.dtype(obj[b"dtype"]).type(obj[b"data"])

    return obj
