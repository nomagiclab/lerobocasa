"""Serve a dummy policy for teleoperation and recording workflows.

This server provides environment metadata and reset states expected by
`lerobocasa.launch.simulation_client`, but action chunks are always zeros.

Example usage:
uv run python examples/dummy_policy_server.py \
    --env-name PickPlaceCounterToCabinet \
    --port 8000
"""

import dataclasses
import json
import logging
import socket
from typing import Any

from dotenv import load_dotenv
import msgpack
import numpy as np
from robosuite.controllers import load_composite_controller_config
import tyro
import websockets.sync.server

import lerobocasa  # noqa: F401  # Registers RoboCasa envs with robosuite.
import robosuite


@dataclasses.dataclass
class Args:
    env_name: str = "PickPlaceCounterToCabinet"
    """RoboCasa environment name"""
    host: str = "0.0.0.0"
    """Host to bind the websocket server"""
    port: int = 8000
    """Port to bind the websocket server"""
    chunk_size: int = 200
    """Number of zero actions returned per action_chunk request"""
    control_freq: float = 20.0
    """Environment control frequency"""
    layout: int | None = None
    """Optional fixed layout id"""
    style: int | None = None
    """Optional fixed style id"""


class DummyPolicyServer:
    def __init__(self, args: Args):
        self._host = args.host
        self._port = args.port
        self._chunk_size = args.chunk_size

        env_kwargs = {
            "robots": "PandaOmron",
            "controller_configs": load_composite_controller_config(robot="PandaOmron"),
            "layout_ids": args.layout,
            "style_ids": args.style,
            "translucent_robot": True,
            "ignore_done": True,
            "use_camera_obs": False,
            "control_freq": args.control_freq,
        }
        self._env_meta = {
            "env_name": args.env_name,
            "env_kwargs": env_kwargs,
        }

        self._env = robosuite.make(
            env_name=args.env_name,
            has_renderer=False,
            has_offscreen_renderer=False,
            renderer="mujoco",
            **env_kwargs,
        )

        self._metadata = {
            "type": "dummy_policy",
            "env_meta": self._env_meta,
            "default_chunk_size": args.chunk_size,
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
            logging.info("Dummy policy server listening at ws://%s:%d", self._host, self._port)
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
        if request_type == "reset_episode":
            return self._reset_episode(int(request["episode_index"]))
        if request_type != "action_chunk":
            raise ValueError(f"Unsupported request_type: {request_type}")

        episode_index = int(request["episode_index"])
        step_index = int(request["step_index"])
        if episode_index < 0:
            raise IndexError(f"episode_index out of range: {episode_index}")
        if step_index < 0:
            raise IndexError(f"step_index out of range: {step_index}")

        actions = np.zeros((self._chunk_size, self._env.action_dim), dtype=np.float32)
        return {
            "actions": actions,
            "episode_index": np.int32(episode_index),
            "start_step": np.int32(step_index),
            "chunk_size": np.int32(self._chunk_size),
            "done": False,
        }

    def _reset_episode(self, episode_index: int) -> dict[str, Any]:
        if episode_index < 0:
            raise IndexError(f"episode_index out of range: {episode_index}")

        self._env.reset()
        ep_meta = self._env.get_ep_meta() if hasattr(self._env, "get_ep_meta") else {}
        initial_state = {
            "states": self._env.sim.get_state().flatten().copy(),
            "model": self._env.model.get_xml(),
            "ep_meta": json.dumps(ep_meta),
        }
        return {
            "episode_index": np.int32(episode_index),
            "initial_state": initial_state,
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
    logging.info("Creating dummy policy server (host: %s, ip: %s)", hostname, local_ip)

    server = DummyPolicyServer(args)
    server.serve_forever()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    main(tyro.cli(Args))
