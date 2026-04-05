import dataclasses
import time

from dotenv import load_dotenv
import tyro

from lerobocasa.launch.common import make_robocasa_env_from_meta
from lerobocasa.launch.common import reset_to
from lerobocasa.launch.common import sleep_to_maintain_rate
from lerobocasa.launch.policy_rpc import PolicyClient


class SimulationClient:
    def __init__(
        self,
        policy_host: str,
        policy_port: int,
        policy_api_key: str | None,
        control_freq: float,
        render: bool,
    ):
        self.control_freq = control_freq
        self.render = render

        self.policy = PolicyClient(host=policy_host, port=policy_port, api_key=policy_api_key)
        env_meta = self.policy.metadata.get("env_meta")
        if env_meta is None:
            raise RuntimeError("Policy server did not provide env_meta")
        self.env = make_robocasa_env_from_meta(env_meta=env_meta, has_renderer=render)

    def _build_action_request(self, episode_index: int, step_index: int) -> dict:
        return {
            "request_type": "action_chunk",
            "episode_index": episode_index,
            "step_index": step_index,
        }

    def _build_reset_request(self, episode_index: int) -> dict:
        return {
            "request_type": "reset_episode",
            "episode_index": episode_index,
        }

    def _run_episode(self, episode_index: int) -> None:
        reset_result = self.policy.infer(self._build_reset_request(episode_index))
        initial_state = reset_result["initial_state"]

        reset_to(self.env, initial_state)

        print(f"Running episode {episode_index:06d}")
        if self.render:
            self.env.render()

        step_index = 0
        while True:
            request = self._build_action_request(
                episode_index=episode_index,
                step_index=step_index,
            )
            result = self.policy.infer(request)
            actions = result["actions"]
            done = bool(result["done"])
            for action in actions:
                start_time = time.time()
                _, _, terminated, truncated = self.env.step(action)

                if self.render:
                    self.env.render()

                sleep_to_maintain_rate(start_time, self.control_freq)
                step_index += 1

            if done:
                return

    def spin(self) -> None:
        episode_index = 0
        while True:
            self._run_episode(episode_index)
            episode_index += 1

    def close(self) -> None:
        self.policy.close()
        self.env.close()


@dataclasses.dataclass
class Args:
    policy_host: str = "127.0.0.1"
    """Replay policy server host"""
    policy_port: int = 8000
    """Replay policy server websocket port"""
    policy_api_key: str | None = None
    """Optional API key for replay policy server"""
    control_freq: float = 20.0
    """Simulation control frequency"""
    render: bool = True
    """Render with on-screen MuJoCo viewer"""


def main() -> None:
    args = tyro.cli(Args)
    node = SimulationClient(
        policy_host=args.policy_host,
        policy_port=args.policy_port,
        policy_api_key=args.policy_api_key,
        control_freq=args.control_freq,
        render=args.render,
    )

    try:
        node.spin()
    finally:
        node.close()


if __name__ == "__main__":
    load_dotenv()
    main()