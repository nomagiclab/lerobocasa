"""Convert raw simulation recordings to a LeRobot v3 dataset.

Example usage (local conversion only):
uv run python -m lerobocasa.converters.convert_recordings_lerobot_v3 \
    --recordings-dir recordings \
    --output-dir /tmp/pickplace_target_v3 \
    --overwrite

Example usage (convert + upload to Hugging Face org robotgeneralist):
uv run python -m lerobocasa.converters.convert_recordings_lerobot_v3 \
    --recordings-dir recordings \
    --output-dir /tmp/pickplace_target_v3 \
    --upload-repo-id robotgeneralist/lerobocasa_custom_recordings \
    --overwrite

When --upload-repo-id is provided, HF_TOKEN is read from .env.
"""

import dataclasses
import gzip
import json
import os
from pathlib import Path
import shutil

from dotenv import load_dotenv
from huggingface_hub import HfApi
from lerobot.datasets.lerobot_dataset import LeRobotDataset
import numpy as np
import tyro

from lerobocasa.launch.recording_io import load_recording

# Original RoboCasa HDF5 action ordering used by recorded simulation actions.
_ACTION_KEY_ORDERING_HDF5 = {
    "end_effector_position": (0, 3),
    "end_effector_rotation": (3, 6),
    "gripper_close": (6, 7),
    "base_motion": (7, 11),
    "control_mode": (11, 12),
}


def _load_modality_dict() -> dict:
    modality_path = (
        Path(__file__).parent.parent / "models/assets/groot_dataset_assets/PandaOmron_modality.json"
    )
    with modality_path.open("r") as f:
        return json.load(f)


def _reorder_hdf5_action_to_lerobot(action_hdf5: np.ndarray, modality_dict: dict) -> np.ndarray:
    action_info = modality_dict["action"]
    sorted_action_keys = sorted(action_info.keys(), key=lambda k: action_info[k]["start"])
    reordered_action = np.zeros_like(action_hdf5)
    for key in sorted_action_keys:
        hdf5_start, hdf5_end = _ACTION_KEY_ORDERING_HDF5[key]
        lerobot_start = action_info[key]["start"]
        lerobot_end = action_info[key]["end"]
        reordered_action[:, lerobot_start:lerobot_end] = action_hdf5[:, hdf5_start:hdf5_end]
    return reordered_action


def _copy_extra_metadata_files(dataset_root: Path) -> None:
    meta_dir = dataset_root / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)

    assets_root = Path(__file__).parent.parent / "models/assets/groot_dataset_assets"
    shutil.copyfile(assets_root / "PandaOmron_modality.json", meta_dir / "modality.json")
    shutil.copyfile(assets_root / "PandaOmron_embodiment.json", meta_dir / "embodiment.json")


def _extract_task_name(recording: dict, fallback: str) -> str:
    initial_state = recording.get("initial_state", {})
    ep_meta = initial_state.get("ep_meta")
    if ep_meta is None:
        return fallback

    if isinstance(ep_meta, str):
        try:
            ep_meta = json.loads(ep_meta)
        except json.JSONDecodeError:
            return fallback

    if isinstance(ep_meta, dict):
        lang = ep_meta.get("lang")
        if isinstance(lang, str) and lang:
            return lang

    return fallback


def _save_episode_extras(dataset_root: Path, episode_index: int, recording: dict) -> None:
    extras_episode_dir = dataset_root / "extras" / f"episode_{episode_index:06d}"
    extras_episode_dir.mkdir(parents=True, exist_ok=True)

    initial_state = recording["initial_state"]
    init_states = np.asarray(initial_state["states"])
    if init_states.ndim == 1:
        states = init_states[None, :]
    else:
        states = init_states

    np.savez_compressed(extras_episode_dir / "states.npz", states=states)

    ep_meta = initial_state.get("ep_meta")
    if isinstance(ep_meta, str):
        try:
            ep_meta = json.loads(ep_meta)
        except json.JSONDecodeError:
            ep_meta = {}
    if ep_meta is None:
        ep_meta = {}
    with (extras_episode_dir / "ep_meta.json").open("w") as f:
        json.dump(ep_meta, f, indent=2)

    model_xml = initial_state.get("model")
    if not isinstance(model_xml, str) or not model_xml:
        raise ValueError(
            f"Recording for episode {episode_index} is missing initial_state.model"
        )
    with gzip.open(extras_episode_dir / "model.xml.gz", "wb") as f:
        f.write(model_xml.encode("utf-8"))


def _save_dataset_meta(dataset_root: Path, env_meta: dict, total_episodes: int) -> None:
    extras_dir = dataset_root / "extras"
    extras_dir.mkdir(parents=True, exist_ok=True)

    dataset_meta = {
        "format": "lerobocasa-recordings-v1",
        "env_args": env_meta,
        "total": int(total_episodes),
    }
    with (extras_dir / "dataset_meta.json").open("w") as f:
        json.dump(dataset_meta, f, indent=2)


def _upload_to_hf(dataset_root: Path, repo_id: str, private: bool) -> None:
    load_dotenv()
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN is missing. Set it in .env to use --upload-repo-id.")

    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", private=private, exist_ok=True)
    api.upload_folder(
        repo_id=repo_id,
        repo_type="dataset",
        folder_path=str(dataset_root),
        commit_message="Upload LeRobot v3 dataset converted from raw recordings",
    )


def _build_dataset(args: "Args") -> Path:
    recordings_dir = Path(args.recordings_dir)
    if not recordings_dir.is_dir():
        raise ValueError(f"recordings_dir is not a directory: {recordings_dir}")

    recording_files = sorted(recordings_dir.glob("*.msgpack"))
    if not recording_files:
        raise ValueError(f"No .msgpack recordings found in: {recordings_dir}")

    dataset_root = Path(args.output_dir)
    if dataset_root.exists():
        if not args.overwrite:
            raise ValueError(
                f"output_dir already exists: {dataset_root}. Use --overwrite to replace it."
            )
        shutil.rmtree(dataset_root)

    modality_dict = _load_modality_dict()

    first_recording = load_recording(recording_files[0])
    env_meta = first_recording.get("env_meta")
    if env_meta is None:
        raise ValueError("First recording is missing env_meta")

    first_actions = np.asarray(first_recording["actions"], dtype=np.float32)
    if first_actions.ndim != 2:
        raise ValueError("Recording actions must be a 2D array")
    action_dim = int(first_actions.shape[1])

    dataset = LeRobotDataset.create(
        repo_id=str(dataset_root),
        robot_type=args.robot_type,
        fps=args.fps,
        features={
            "action": {"dtype": "float32", "shape": (action_dim,)},
        },
    )

    fallback_task = str(env_meta.get("env_name", "recording"))

    for episode_index, recording_path in enumerate(recording_files):
        recording = load_recording(recording_path)

        current_env_meta = recording.get("env_meta")
        if current_env_meta != env_meta:
            raise ValueError(
                f"All recordings must share identical env_meta. Mismatch in: {recording_path}"
            )

        actions_hdf5 = np.asarray(recording["actions"], dtype=np.float32)
        if actions_hdf5.ndim != 2:
            raise ValueError(f"actions must be 2D in recording: {recording_path}")
        if actions_hdf5.shape[1] != action_dim:
            raise ValueError(
                f"Inconsistent action dimension in {recording_path}: "
                f"expected {action_dim}, got {actions_hdf5.shape[1]}"
            )

        actions_lerobot = _reorder_hdf5_action_to_lerobot(actions_hdf5, modality_dict).astype(
            np.float32
        )
        task_name = _extract_task_name(recording, fallback=fallback_task)

        for action in actions_lerobot:
            dataset.add_frame({"action": action, "task": task_name})
        dataset.save_episode()

        _save_episode_extras(dataset_root, episode_index, recording)

    dataset.finalize()
    _copy_extra_metadata_files(dataset_root)
    _save_dataset_meta(dataset_root, env_meta=env_meta, total_episodes=len(recording_files))

    print(f"Created LeRobot v3 dataset at: {dataset_root}")
    print(f"Episodes: {len(recording_files)}")
    print(f"Action dimension: {action_dim}")
    return dataset_root


@dataclasses.dataclass
class Args:
    recordings_dir: str
    """Directory containing raw .msgpack recordings"""
    output_dir: str
    """Output directory for the converted LeRobot v3 dataset"""
    robot_type: str = "PandaOmron"
    """Robot type stored in LeRobot metadata"""
    fps: int = 20
    """Dataset control frequency"""
    overwrite: bool = False
    """Overwrite output_dir if it already exists"""
    upload_repo_id: str | None = None
    """Optional HF dataset repo id (e.g. robotgeneralist/MyDataset) to upload after conversion"""
    upload_private: bool = False
    """Create the HF dataset repo as private when uploading"""


def main(args: Args) -> None:
    dataset_root = _build_dataset(args)
    if args.upload_repo_id:
        _upload_to_hf(dataset_root=dataset_root, repo_id=args.upload_repo_id, private=args.upload_private)
        print(f"Uploaded dataset to hf.co/datasets/{args.upload_repo_id}")


if __name__ == "__main__":
    main(tyro.cli(Args))
