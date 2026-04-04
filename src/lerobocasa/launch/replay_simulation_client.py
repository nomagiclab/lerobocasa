import dataclasses
import time

from dotenv import load_dotenv
import tyro

from lerobocasa.launch.common import make_robocasa_env_from_meta
from lerobocasa.launch.common import reset_to
from lerobocasa.launch.common import sleep_to_maintain_rate
from lerobocasa.launch.replay_policy_rpc import PolicyClient


class ReplaySimulationClient:
    def __init__(
        self,
        policy_host: str,
        policy_port: int,
        policy_api_key: str | None,
        execution_horizon: int,
        control_freq: float,
        render: bool,
        max_episodes: int | None,
    ):
        self.execution_horizon = execution_horizon
        self.control_freq = control_freq
        self.render = render
        self.max_episodes = max_episodes

        self.policy = PolicyClient(host=policy_host, port=policy_port, api_key=policy_api_key)
        env_meta = self.policy.metadata.get("env_meta")
        if env_meta is None:
            raise RuntimeError("Policy server did not provide env_meta")
        self.env = make_robocasa_env_from_meta(env_meta=env_meta, has_renderer=render)
        self.num_episodes = int(self.policy.metadata.get("num_episodes", 0))

    def _build_action_request(self, episode_index: int, step_index: int) -> dict:
        return {
            "request_type": "action_chunk",
            "episode_index": episode_index,
            "step_index": step_index,
            "execution_horizon": self.execution_horizon,
        }

    def _build_reset_request(self, episode_index: int) -> dict:
        return {
            "request_type": "reset_episode",
            "episode_index": episode_index,
        }

    def _run_episode(self, episode_index: int) -> None:
        reset_result = self.policy.infer(self._build_reset_request(episode_index))
        initial_state = reset_result["initial_state"]
        num_steps = int(reset_result["num_steps"])

        reset_to(self.env, initial_state)

        print(f"Running episode {episode_index:06d} with {num_steps} steps")
        if self.render:
            self.env.render()

        step_index = 0
        while step_index < num_steps:
            request = self._build_action_request(
                episode_index=episode_index,
                step_index=step_index,
            )
            result = self.policy.infer(request)
            actions = result["actions"]

            if len(actions) == 0:
                raise RuntimeError(
                    f"Policy server returned zero actions at episode {episode_index} step {step_index}"
                )

            for action in actions:
                if step_index >= num_steps:
                    break

                start_time = time.time()
                self.env.step(action)

                if self.render:
                    self.env.render()

                sleep_to_maintain_rate(start_time, self.control_freq)
                step_index += 1

    def spin(self) -> None:
        num_episodes = self.num_episodes
        if self.max_episodes is not None:
            num_episodes = min(num_episodes, self.max_episodes)

        for episode_index in range(num_episodes):
            self._run_episode(episode_index)

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
    execution_horizon: int = 15
    """How many actions from each policy chunk to execute"""
    control_freq: float = 20.0
    """Simulation control frequency"""
    render: bool = True
    """Render with on-screen MuJoCo viewer"""
    max_episodes: int | None = None
    """Optional cap on number of episodes to replay"""


def main() -> None:
    args = tyro.cli(Args)
    node = ReplaySimulationClient(
        policy_host=args.policy_host,
        policy_port=args.policy_port,
        policy_api_key=args.policy_api_key,
        execution_horizon=args.execution_horizon,
        control_freq=args.control_freq,
        render=args.render,
        max_episodes=args.max_episodes,
    )

    try:
        node.spin()
    finally:
        node.close()


if __name__ == "__main__":
    load_dotenv()
    main()
