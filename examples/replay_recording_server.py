"""Serve actions from a simple simulation recording file.

Example usage:
uv run python examples/replay_recording_server.py \
    --recordings_dir recordings \
    --port 8000
"""

import dataclasses
import logging
from pathlib import Path
import socket
from typing import Any

from dotenv import load_dotenv
import msgpack
import numpy as np
import tyro
import websockets.sync.server

from lerobocasa.launch.recording_io import load_recording


@dataclasses.dataclass
class Args:
    recordings_dir: str
    """Directory with .msgpack recordings produced by simulation_client"""
    host: str = "0.0.0.0"
    """Host to bind the replay websocket server"""
    port: int = 8000
    """Port to bind the replay websocket server"""
    chunk_size: int = 200
    """Number of actions returned per action_chunk request"""


class ReplayRecordingServer:
    def __init__(self, recordings_dir: str, host: str, port: int, chunk_size: int):
        self._host = host
        self._port = port
        self._default_chunk_size = chunk_size

        recordings_path = Path(recordings_dir)
        if not recordings_path.is_dir():
            raise ValueError(f"recordings_dir is not a directory: {recordings_dir}")

        recording_files = sorted(recordings_path.glob("*.msgpack"))
        if not recording_files:
            raise ValueError(f"No .msgpack recordings found in: {recordings_dir}")

        self._episodes: list[dict[str, Any]] = []
        for file_path in recording_files:
            recording = load_recording(file_path)
            self._episodes.append(
                {
                    "file": str(file_path),
                    "actions": np.asarray(recording["actions"], dtype=np.float32),
                    "initial_state": recording["initial_state"],
                    "env_meta": recording["env_meta"],
                }
            )

        self._metadata = {
            "type": "replay_recording",
            "recordings_dir": recordings_dir,
            "num_episodes": len(self._episodes),
            "default_chunk_size": chunk_size,
            "env_meta": self._episodes[0]["env_meta"],
        }
        self._packer = msgpack.Packer(default=_pack_array)

    def serve_forever(self) -> None:
        with websockets.sync.server.serve(
            self._handle_connection,
            host=self._host,
            port=self._port,
            compression=None,
            max_size=None,
        ) as server:
            logging.info("Replay recording server listening at ws://%s:%d", self._host, self._port)
            server.serve_forever()

    def _handle_connection(self, websocket) -> None:
        websocket.send(self._packer.pack(self._metadata))
        while True:
            payload = websocket.recv()
            if isinstance(payload, str):
                websocket.send("Expected binary msgpack request")
                continue

            try:
                request = msgpack.unpackb(payload, object_hook=_unpack_array)
                response = self._infer(request)
                websocket.send(self._packer.pack(response))
            except Exception as exc:
                websocket.send(str(exc))

    def _infer(self, request: dict[str, Any]) -> dict[str, Any]:
        request_type = request["request_type"]
        episode_index = int(request["episode_index"])
        if episode_index < 0:
            raise IndexError(f"episode_index out of range: {episode_index}")
        episode_index = episode_index % len(self._episodes)
        episode = self._episodes[episode_index]

        if request_type == "reset_episode":
            return {
                "episode_index": np.int32(episode_index),
                "initial_state": episode["initial_state"],
            }
        if request_type != "action_chunk":
            raise ValueError(f"Unsupported request_type: {request_type}")

        actions = episode["actions"]
        step_index = int(request["step_index"])
        if step_index < 0 or step_index > len(actions):
            raise IndexError(f"step_index out of range: {step_index}")

        if step_index == len(actions):
            return {
                "actions": np.empty((0, 0), dtype=np.float32),
                "episode_index": np.int32(episode_index),
                "start_step": np.int32(step_index),
                "chunk_size": np.int32(0),
                "done": True,
            }

        frame_to = min(step_index + self._default_chunk_size, len(actions))
        chunk = actions[step_index:frame_to]
        return {
            "actions": chunk,
            "episode_index": np.int32(episode_index),
            "start_step": np.int32(step_index),
            "chunk_size": np.int32(len(chunk)),
            "done": frame_to >= len(actions),
        }


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


def main(args: Args) -> None:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    logging.info("Creating replay recording server (host: %s, ip: %s)", hostname, local_ip)

    server = ReplayRecordingServer(
        recordings_dir=args.recordings_dir,
        host=args.host,
        port=args.port,
        chunk_size=args.chunk_size,
    )
    server.serve_forever()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    main(tyro.cli(Args))
