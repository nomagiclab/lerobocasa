"""Serve replay actions from a lerobot dataset.

This script mirrors the websocket client/server architecture used by lerobosuite,
but instead of model inference it returns recorded dataset actions.

Example usage:
uv run --with lerobot examples/replay_policy_server.py \
    --dataset_repo_id robotgeneralist/PickPlaceCounterToCabinet_pretrain \
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
import tyro
import websockets.sync.server

from lerobot.datasets.lerobot_dataset import LeRobotDataset
import lerobocasa.utils.lerobot_utils as LU
from lerobocasa.utils.lerobot_utils import reorder_lerobot_action


@dataclasses.dataclass
class Args:
    dataset_repo_id: str = "robotgeneralist/PickPlaceCounterToCabinet_pretrain"
    """Hugging Face dataset repo id"""
    host: str = "0.0.0.0"
    """Host to bind the replay websocket server"""
    port: int = 8000
    """Port to bind the replay websocket server"""
    chunk_size: int = 15
    """Default action chunk size when request does not provide execution_horizon"""


class ReplayPolicyServer:
    def __init__(self, dataset_repo_id: str, host: str, port: int, chunk_size: int):
        self._dataset_repo_id = dataset_repo_id
        self._host = host
        self._port = port
        self._default_chunk_size = chunk_size

        # Use explicit branch to avoid requiring HF tags for codebase version lookup.
        self._dataset = LeRobotDataset(
            repo_id=dataset_repo_id,
            revision="main",
            download_videos=True,
        )
        self._dataset_root = self._dataset.root
        self._env_meta = LU.get_env_metadata(self._dataset_root)
        self._episode_ranges = [
            (int(row["dataset_from_index"]), int(row["dataset_to_index"]))
            for row in self._dataset.meta.episodes
        ]

        self._metadata = {
            "type": "replay_policy",
            "dataset_repo_id": dataset_repo_id,
            "num_episodes": len(self._episode_ranges),
            "default_chunk_size": chunk_size,
            "env_meta": self._env_meta,
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
            logging.info("Replay policy server listening at ws://%s:%d", self._host, self._port)
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
        request_type = request.get("request_type", "action_chunk")
        if request_type == "reset_episode":
            return self._reset_episode(int(request["episode_index"]))

        episode_index = int(request["episode_index"])
        step_index = int(request["step_index"])
        chunk_size = int(request.get("execution_horizon", self._default_chunk_size))

        if episode_index < 0 or episode_index >= len(self._episode_ranges):
            raise IndexError(f"episode_index out of range: {episode_index}")

        start_idx, end_idx = self._episode_ranges[episode_index]
        episode_len = end_idx - start_idx
        if step_index < 0 or step_index > episode_len:
            raise IndexError(
                f"step_index out of range for episode {episode_index}: {step_index}"
            )

        frame_from = start_idx + step_index
        frame_to = min(start_idx + step_index + chunk_size, end_idx)
        actions_lerobot = np.stack(
            [np.asarray(self._dataset[idx]["action"]) for idx in range(frame_from, frame_to)]
        )
        chunk = reorder_lerobot_action(action_lerobot=actions_lerobot, dataset=self._dataset_root)
        return {
            "actions": chunk.astype(np.float32),
            "episode_index": np.int32(episode_index),
            "start_step": np.int32(step_index),
            "chunk_size": np.int32(len(chunk)),
        }

    def _reset_episode(self, episode_index: int) -> dict[str, Any]:
        if episode_index < 0 or episode_index >= len(self._episode_ranges):
            raise IndexError(f"episode_index out of range: {episode_index}")

        states = LU.get_episode_states(self._dataset_root, episode_index)
        initial_state = {
            "states": states[0],
            "model": LU.get_episode_model_xml(self._dataset_root, episode_index),
            "ep_meta": json.dumps(LU.get_episode_meta(self._dataset_root, episode_index)),
        }
        return {
            "episode_index": np.int32(episode_index),
            "num_steps": np.int32(states.shape[0]),
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
    logging.info("Creating replay policy server (host: %s, ip: %s)", hostname, local_ip)

    server = ReplayPolicyServer(
        dataset_repo_id=args.dataset_repo_id,
        host=args.host,
        port=args.port,
        chunk_size=args.chunk_size,
    )
    server.serve_forever()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    main(tyro.cli(Args))
