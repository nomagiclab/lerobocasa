from copy import deepcopy
import time

import numpy as np

from lerobocasa.wrappers.enclosing_wall_render_wrapper import EnclosingWallHotkeyHandler


def is_empty_input_spacemouse(action_dict):
    if not np.all(action_dict["right_delta"] == 0):
        return False
    if "base_mode" in action_dict and action_dict["base_mode"] != -1:
        return False
    if "base" in action_dict and not np.all(action_dict["base"] == 0):
        return False

    return True


def collect_human_trajectory(
    env,
    device,
    arm,
    env_configuration,
    mirror_actions,
    render=True,
    max_fr=None,
    print_info=True,
):
    """Run an interactive teleop trajectory and return `(ep_directory, discard_traj)`.

    This helper intentionally stays lightweight and independent from legacy dataset
    wrappers / robomimic conversion code.
    """

    env.reset()

    ep_meta = env.get_ep_meta()
    lang = ep_meta.get("lang", None)
    if print_info and lang is not None:
        print(f"Instruction: {lang}")

    if render:
        env.render()

    task_completion_hold_count = -1
    device.start_control()

    nonzero_ac_seen = False

    all_prev_gripper_actions = [
        {
            f"{robot_arm}_gripper": np.repeat([0], robot.gripper[robot_arm].dof)
            for robot_arm in robot.arms
            if robot.gripper[robot_arm].dof > 0
        }
        for robot in env.robots
    ]

    zero_action = np.zeros(env.action_dim)
    env.step(zero_action)

    discard_traj = False
    wall_hotkeys = EnclosingWallHotkeyHandler(env)

    while True:
        start = time.time()

        if wall_hotkeys.consume_pending(render=render):
            continue

        active_robot = env.robots[device.active_robot]

        input_ac_dict = device.input2action(mirror_actions=mirror_actions)
        if input_ac_dict is None:
            discard_traj = True
            break

        action_dict = deepcopy(input_ac_dict)

        for robot_arm in active_robot.arms:
            controller_input_type = active_robot.part_controllers[robot_arm].input_type
            if controller_input_type == "delta":
                action_dict[robot_arm] = input_ac_dict[f"{robot_arm}_delta"]
            elif controller_input_type == "absolute":
                action_dict[robot_arm] = input_ac_dict[f"{robot_arm}_abs"]
            else:
                raise ValueError(f"Unsupported controller input type: {controller_input_type}")

        if is_empty_input_spacemouse(action_dict):
            if not nonzero_ac_seen:
                if render:
                    env.render()
                continue
        else:
            nonzero_ac_seen = True

        env_action = [
            robot.create_action_vector(all_prev_gripper_actions[i])
            for i, robot in enumerate(env.robots)
        ]
        env_action[device.active_robot] = active_robot.create_action_vector(action_dict)
        env_action = np.concatenate(env_action)

        env.step(env_action)
        if render:
            env.render()

        if task_completion_hold_count == 0:
            break

        if env._check_success():
            if task_completion_hold_count > 0:
                task_completion_hold_count -= 1
            else:
                task_completion_hold_count = 15
        else:
            task_completion_hold_count = -1

        if max_fr is not None:
            elapsed = time.time() - start
            diff = 1 / max_fr - elapsed
            if diff > 0:
                time.sleep(diff)

    if nonzero_ac_seen and hasattr(env, "ep_directory"):
        ep_directory = env.ep_directory
    else:
        ep_directory = None

    env.close()

    return ep_directory, discard_traj
