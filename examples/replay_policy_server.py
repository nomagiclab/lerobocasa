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


class ReplayPolicyServer:
    def __init__(self, dataset_repo_id: str, host: str, port: int):
        self._dataset_repo_id = dataset_repo_id
        self._host = host
        self._port = port

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
        episode_index = 0
        while True:
            payload = websocket.recv()
            if isinstance(payload, str):
                websocket.send("Expected binary msgpack request")
                continue

            try:
                msgpack.unpackb(payload, object_hook=_unpack_array)
                response = self._infer(episode_index)
                episode_index = (episode_index + 1) % len(self._episode_ranges)
                websocket.send(self._packer.pack(response))
            except Exception as exc:
                websocket.send(str(exc))

    def _infer(self, episode_index: int) -> dict[str, Any]:
        start_idx, end_idx = self._episode_ranges[episode_index]
        actions_lerobot = np.stack(
            [np.asarray(self._dataset[idx]["action"]) for idx in range(start_idx, end_idx)]
        )
        actions = reorder_lerobot_action(action_lerobot=actions_lerobot, dataset=self._dataset_root)
        states = LU.get_episode_states(self._dataset_root, episode_index)
        return {
            "actions": actions.astype(np.float32),
            "done": True,
            "initial_state": {
                "states": states[0],
                "model": LU.get_episode_model_xml(self._dataset_root, episode_index),
                "ep_meta": json.dumps(LU.get_episode_meta(self._dataset_root, episode_index)),
            },
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
    )
    server.serve_forever()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    main(tyro.cli(Args))
