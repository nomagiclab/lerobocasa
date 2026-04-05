import dataclasses
import time
from copy import deepcopy

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
        self._hotkeys = _ClientHotkeys()
        self._teleop_device = _create_keyboard_device(self.env)
        self._all_prev_gripper_actions = []

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
            "Enter toggles recording. T toggles teleoperation."
        )

        step_index = 0
        teleop_active = False
        policy_actions: list[np.ndarray] = []
        policy_chunk_done = False

        self._reset_teleop_state()

        recording_active = False
        recording_start_step = 0
        recording_initial_state: dict | None = None
        recorded_actions: list[np.ndarray] = []

        while True:
            if self._hotkeys.consume_record_toggle_request():
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

            if self._hotkeys.consume_teleop_toggle_request():
                teleop_active = not teleop_active
                policy_actions = []
                policy_chunk_done = False
                if teleop_active:
                    self._teleop_device.start_control()
                    print("Teleoperation ON")
                else:
                    print("Teleoperation OFF")

            if teleop_active:
                action = self._build_teleop_action()
                self._step_env(action)
                if recording_active:
                    recorded_actions.append(np.asarray(action, dtype=np.float32))
                step_index += 1
                continue

            if not policy_actions:
                request = self._build_action_request(
                    episode_index=episode_index,
                    step_index=step_index,
                )
                result = self.policy.infer(request)
                policy_actions = [np.asarray(action, dtype=np.float32) for action in result["actions"]]
                policy_chunk_done = bool(result["done"])

                if not policy_actions and policy_chunk_done:
                    if recording_active:
                        self._save_recording(
                            episode_index=episode_index,
                            start_step=recording_start_step,
                            initial_state=recording_initial_state,
                            recorded_actions=recorded_actions,
                        )
                    print("Episode finished before manual stop.")
                    break

                if not policy_actions:
                    continue

            action = policy_actions.pop(0)
            self._step_env(action)
            if recording_active:
                recorded_actions.append(np.asarray(action, dtype=np.float32))
            step_index += 1

            if not policy_actions and policy_chunk_done:
                if recording_active:
                    self._save_recording(
                        episode_index=episode_index,
                        start_step=recording_start_step,
                        initial_state=recording_initial_state,
                        recorded_actions=recorded_actions,
                    )
                print("Episode finished before manual stop.")
                break

    def _step_env(self, action: np.ndarray) -> None:
        start_time = time.time()
        self.env.step(action)
        if self.render:
            self.env.render()
        sleep_to_maintain_rate(start_time, self.control_freq)

    def _reset_teleop_state(self) -> None:
        self._teleop_device.start_control()
        self._all_prev_gripper_actions = [
            {
                f"{robot_arm}_gripper": np.repeat([0], robot.gripper[robot_arm].dof)
                for robot_arm in robot.arms
                if robot.gripper[robot_arm].dof > 0
            }
            for robot in self.env.robots
        ]

    def _build_teleop_action(self) -> np.ndarray:
        input_ac_dict = self._teleop_device.input2action(mirror_actions=True)
        if input_ac_dict is None:
            return np.zeros(self.env.action_dim, dtype=np.float32)

        active_robot_idx = self._teleop_device.active_robot
        active_robot = self.env.robots[active_robot_idx]
        action_dict = deepcopy(input_ac_dict)

        for arm in active_robot.arms:
            controller_input_type = active_robot.part_controllers[arm].input_type
            if controller_input_type == "delta":
                action_dict[arm] = input_ac_dict[f"{arm}_delta"]
            elif controller_input_type == "absolute":
                action_dict[arm] = input_ac_dict[f"{arm}_abs"]
            else:
                raise ValueError(f"Unsupported controller input type: {controller_input_type}")

        for arm in active_robot.arms:
            gripper_key = f"{arm}_gripper"
            if gripper_key in action_dict and gripper_key in self._all_prev_gripper_actions[active_robot_idx]:
                self._all_prev_gripper_actions[active_robot_idx][gripper_key] = action_dict[gripper_key]

        env_action = [
            robot.create_action_vector(self._all_prev_gripper_actions[i])
            for i, robot in enumerate(self.env.robots)
        ]
        env_action[active_robot_idx] = active_robot.create_action_vector(action_dict)
        return np.asarray(np.concatenate(env_action), dtype=np.float32)

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
        self._hotkeys.close()
        if hasattr(self._teleop_device, "listener"):
            self._teleop_device.listener.stop()
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


def _create_keyboard_device(env):
    from robosuite.devices import Keyboard

    return Keyboard(env=env, pos_sensitivity=4.0, rot_sensitivity=4.0)


class _ClientHotkeys:
    def __init__(self) -> None:
        self._pending_record_toggles = 0
        self._pending_teleop_toggles = 0
        self._listener = Listener(on_release=self._on_release)
        self._listener.start()

    def _on_release(self, key) -> None:
        if key == Key.enter:
            self._pending_record_toggles += 1
            return
        if hasattr(key, "char") and key.char is not None and key.char.lower() == "t":
            self._pending_teleop_toggles += 1

    def consume_record_toggle_request(self) -> bool:
        if self._pending_record_toggles <= 0:
            return False
        self._pending_record_toggles -= 1
        return True

    def consume_teleop_toggle_request(self) -> bool:
        if self._pending_teleop_toggles <= 0:
            return False
        self._pending_teleop_toggles -= 1
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