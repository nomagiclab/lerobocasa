import dataclasses
import time

from dotenv import load_dotenv
import tyro
import numpy as np
from pynput.keyboard import Key
from pynput.keyboard import Listener

from lerobocasa.launch.common import make_robocasa_env_from_meta
from lerobocasa.launch.common import reset_to
from lerobocasa.launch.common import sleep_to_maintain_rate
from lerobocasa.launch.policy_rpc import PolicyClient
from lerobocasa.launch.recording_io import save_recording


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
        self._record_toggle_hotkey = _RecordToggleHotkey()

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
        episode_initial_state = reset_result["initial_state"]

        reset_to(self.env, episode_initial_state)

        print(
            f"Running episode {episode_index:06d}. "
            "Press Enter to start/stop recording at any time (viewer focus is fine)."
        )

        step_index = 0
        recording_active = False
        recording_start_step = 0
        recording_initial_state: dict | None = None
        recorded_actions: list[np.ndarray] = []

        while True:
            request = self._build_action_request(
                episode_index=episode_index,
                step_index=step_index,
            )
            result = self.policy.infer(request)
            actions = result["actions"]
            done = bool(result["done"])

            for action in actions:
                if self._record_toggle_hotkey.consume_toggle_request():
                    if not recording_active:
                        recording_active = True
                        recording_start_step = step_index
                        recording_initial_state = {
                            "states": self.env.sim.get_state().flatten().copy(),
                            "model": episode_initial_state.get("model"),
                            "ep_meta": episode_initial_state.get("ep_meta"),
                        }
                        recorded_actions = []
                        print(f"Recording started at step {recording_start_step}.")
                    else:
                        recording_active = False
                        self._save_recording(
                            episode_index=episode_index,
                            start_step=recording_start_step,
                            initial_state=recording_initial_state,
                            recorded_actions=recorded_actions,
                        )
                        recorded_actions = []
                        recording_initial_state = None

                start_time = time.time()
                self.env.step(action)
                if self.render:
                    self.env.render()
                if recording_active:
                    recorded_actions.append(np.asarray(action, dtype=np.float32))
                sleep_to_maintain_rate(start_time, self.control_freq)
                step_index += 1

            if done:
                if recording_active:
                    self._save_recording(
                        episode_index=episode_index,
                        start_step=recording_start_step,
                        initial_state=recording_initial_state,
                        recorded_actions=recorded_actions,
                    )
                print("Episode finished before manual stop.")
                break

    def _save_recording(
        self,
        episode_index: int,
        start_step: int,
        initial_state: dict | None,
        recorded_actions: list[np.ndarray],
    ) -> None:
        if initial_state is None:
            return
        if not recorded_actions:
            print("Recording was empty. Nothing saved.")
            return

        actions_np = np.stack(recorded_actions)
        recording = {
            "episode_index": np.int32(episode_index),
            "start_step": np.int32(start_step),
            "env_meta": self.policy.metadata.get("env_meta"),
            "initial_state": initial_state,
            "actions": actions_np,
            "control_freq": np.float32(self.control_freq),
        }
        path = save_recording(recording, output_dir="recordings")
        print(f"Saved recording: {path}")

    def spin(self) -> None:
        episode_index = 0
        while True:
            self._run_episode(episode_index)
            episode_index += 1

    def close(self) -> None:
        self._record_toggle_hotkey.close()
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


class _RecordToggleHotkey:
    def __init__(self) -> None:
        self._pending_toggles = 0
        self._listener = Listener(on_release=self._on_release)
        self._listener.start()

    def _on_release(self, key) -> None:
        if key == Key.enter:
            self._pending_toggles += 1

    def consume_toggle_request(self) -> bool:
        if self._pending_toggles <= 0:
            return False
        self._pending_toggles -= 1
        return True

    def close(self) -> None:
        self._listener.stop()


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