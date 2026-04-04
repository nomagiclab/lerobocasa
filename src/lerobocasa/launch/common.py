import json
import time
from pathlib import Path

import numpy as np
import robosuite


def sleep_to_maintain_rate(start_time: float, hz: float) -> None:
    sleep_time = (1.0 / hz) - (time.time() - start_time)
    if sleep_time > 0:
        time.sleep(sleep_time)


def load_episode_initial_state(dataset_dir: Path, episode_index: int) -> dict:
    import lerobocasa.utils.lerobot_utils as LU

    states = LU.get_episode_states(dataset_dir, episode_index)
    return {
        "states": states[0],
        "model": LU.get_episode_model_xml(dataset_dir, episode_index),
        "ep_meta": json.dumps(LU.get_episode_meta(dataset_dir, episode_index)),
    }


def load_episode_states(dataset_dir: Path, episode_index: int) -> np.ndarray:
    import lerobocasa.utils.lerobot_utils as LU

    return LU.get_episode_states(dataset_dir, episode_index)


def make_robocasa_env(dataset_dir: Path, has_renderer: bool):
    import lerobocasa.utils.lerobot_utils as LU

    env_meta = LU.get_env_metadata(dataset_dir)
    return make_robocasa_env_from_meta(env_meta=env_meta, has_renderer=has_renderer)


def make_robocasa_env_from_meta(env_meta: dict, has_renderer: bool):
    env_kwargs = dict(env_meta["env_kwargs"])
    env_kwargs["env_name"] = env_meta["env_name"]
    env_kwargs["renderer"] = "mjviewer"
    env_kwargs["has_renderer"] = has_renderer
    env_kwargs["has_offscreen_renderer"] = False
    env_kwargs["use_camera_obs"] = False
    return robosuite.make(**env_kwargs)


def reset_to(env, state: dict) -> None:
    if "model" in state:
        if state.get("ep_meta") is not None:
            ep_meta = json.loads(state["ep_meta"])
        else:
            ep_meta = {}

        if hasattr(env, "set_attrs_from_ep_meta"):
            env.set_attrs_from_ep_meta(ep_meta)
        elif hasattr(env, "set_ep_meta"):
            env.set_ep_meta(ep_meta)

        env.reset()
        robosuite_version_id = int(robosuite.__version__.split(".")[1])
        if robosuite_version_id <= 3:
            from robosuite.utils.mjcf_utils import postprocess_model_xml

            xml = postprocess_model_xml(state["model"])
        else:
            xml = env.edit_model_xml(state["model"])

        env.reset_from_xml_string(xml)
        env.sim.reset()

    if "states" in state:
        env.sim.set_state_from_flattened(state["states"])
        env.sim.forward()

    if hasattr(env, "update_sites"):
        env.update_sites()
    if hasattr(env, "update_state"):
        env.update_state()
