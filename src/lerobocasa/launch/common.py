import json
import time

import robosuite


def sleep_to_maintain_rate(start_time: float, hz: float) -> None:
    sleep_time = (1.0 / hz) - (time.time() - start_time)
    if sleep_time > 0:
        time.sleep(sleep_time)


def make_robocasa_env_from_meta(env_meta: dict, has_renderer: bool):
    env_kwargs = dict(env_meta["env_kwargs"])
    env_kwargs["env_name"] = env_meta["env_name"]
    env_kwargs["renderer"] = "mjviewer"
    env_kwargs["has_renderer"] = has_renderer
    env_kwargs["has_offscreen_renderer"] = True
    env_kwargs["use_camera_obs"] = True
    env_kwargs.setdefault(
        "camera_names",
        ["robot0_eye_in_hand", "robot0_agentview_left", "robot0_agentview_right"],
    )
    env_kwargs.setdefault("camera_heights", 256)
    env_kwargs.setdefault("camera_widths", 256)
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
        if env.sim is None:
            env.reset()
        env.sim.set_state_from_flattened(state["states"])
        env.sim.forward()

    if hasattr(env, "update_sites"):
        env.update_sites()
    if hasattr(env, "update_state"):
        env.update_state()
