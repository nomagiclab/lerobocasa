"""Serve a policy for robosuite.

This script can be used together with a separate lerobosuite repository:
https://github.com/nomagiclab/lerobosuite
See information there.

Example usage:
devcontainer exec --workspace-folder . -- bash -lc 'uv run scripts/serve_policy_robosuite.py --preset LIFT'
"""

import dataclasses
import enum
import logging
import socket

from dotenv import load_dotenv
import tyro

from openpi.policies import policy as _policy
from openpi.policies import policy_config as _policy_config
from openpi.serving import websocket_policy_server
from openpi.shared.download import download_checkpoint_from_hf
from openpi.training import config as _config


class RobosuitePreset(enum.Enum):
    LIFT = "lift"
    CAN = "can"
    SQUARE = "square"


@dataclasses.dataclass(frozen=True)
class PresetCheckpoint:
    config_name: str
    repo_id: str
    checkpoint_path: str
    default_prompt: str


PRESET_CHECKPOINTS: dict[RobosuitePreset, PresetCheckpoint] = {
    RobosuitePreset.CAN: PresetCheckpoint(
        config_name="pi0_robosuite_can",
        repo_id="robotgeneralist/pi0_robosuite",
        checkpoint_path="robosuite_can/2000",
        default_prompt="pick the can and place it in the bin",
    ),
}


@dataclasses.dataclass
class Args:
    preset: RobosuitePreset = RobosuitePreset.LIFT
    """Robosuite task preset"""
    host: str = "0.0.0.0"
    """Host to bind the policy websocket server"""
    port: int = 8000
    """Port to bind the policy websocket server"""
    revision: str = "main"
    """Revision in the Hugging Face repository"""
    config_name: str | None = None
    """Optional override for training config name"""
    repo_id: str | None = None
    """Optional override for Hugging Face repo id"""
    checkpoint_path: str | None = None
    """Optional override for checkpoint path in the Hugging Face repo"""
    default_prompt: str | None = None
    """Optional default prompt override"""
    record: bool = False
    """Record policy requests and actions to policy_records/"""


def _resolve_checkpoint(args: Args) -> PresetCheckpoint:
    preset = PRESET_CHECKPOINTS[args.preset]
    return PresetCheckpoint(
        config_name=args.config_name or preset.config_name,
        repo_id=args.repo_id or preset.repo_id,
        checkpoint_path=args.checkpoint_path or preset.checkpoint_path,
        default_prompt=args.default_prompt or preset.default_prompt,
    )


def main(args: Args) -> None:
    checkpoint = _resolve_checkpoint(args)

    checkpoint_dir = download_checkpoint_from_hf(
        repo_id=checkpoint.repo_id,
        revision=args.revision,
        checkpoint_path=checkpoint.checkpoint_path,
    )

    policy = _policy_config.create_trained_policy(
        _config.get_config(checkpoint.config_name),
        checkpoint_dir,
        default_prompt=checkpoint.default_prompt,
    )
    policy_metadata = policy.metadata

    if args.record:
        policy = _policy.PolicyRecorder(policy, "policy_records")

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    logging.info("Creating robosuite policy server (host: %s, ip: %s)", hostname, local_ip)

    server = websocket_policy_server.WebsocketPolicyServer(
        policy=policy,
        host=args.host,
        port=args.port,
        metadata=policy_metadata,
    )
    server.serve_forever()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    main(tyro.cli(Args))