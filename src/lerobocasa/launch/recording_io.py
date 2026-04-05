import datetime as _dt
from pathlib import Path
from typing import Any

import msgpack
import numpy as np


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


def save_recording(recording: dict[str, Any], output_dir: str | Path) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    episode_index = int(recording.get("episode_index", 0))
    file_path = output / f"recording_ep{episode_index:06d}_{timestamp}.msgpack"

    payload = {
        "format": "lerobocasa-simple-recording-v1",
        "created_at": _dt.datetime.now().isoformat(timespec="seconds"),
        **recording,
    }
    with file_path.open("wb") as f:
        f.write(msgpack.packb(payload, default=_pack_array))
    return file_path


def load_recording(path: str | Path) -> dict[str, Any]:
    with Path(path).open("rb") as f:
        return msgpack.unpackb(f.read(), object_hook=_unpack_array)
