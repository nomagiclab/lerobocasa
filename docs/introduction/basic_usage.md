# Basic Usage

<div class="admonition warning">
<p class="admonition-title">Attention Mac users!</p>

For these scripts, Mac users need to prepend the "python" command with "mj": `mjpython ...`
</div>

-------
### Gym Interface

The following script shows how to create a gym environment and to run random rollouts:

```py
import gymnasium as gym
import robocasa
from robocasa.utils.env_utils import run_random_rollouts

env = gym.make(
    "robocasa/PickPlaceCounterToCabinet",
    split="pretrain", # use 'pretrain' or 'target' kitchen scenes and objects
    seed=0 # seed environment as needed. set seed=None to run unseeded
)

# run rollouts with random actions and save video
run_random_rollouts(
    env, num_rollouts=3, num_steps=100, video_path="/tmp/test.mp4"
)
```

-------
### Explore kitchen layouts and styles
Explore kitchen layouts (G-shaped, U-shaped, etc) and kitchen styles (mediterranean, industrial, etc):
```
python -m robocasa.demos.demo_kitchen_scenes
```

-------
### Replay recorded datasets (server-client)
Run replay in two terminals using the policy server <-> simulation client flow:

```
python examples/replay_policy_server.py --dataset_repo_id robotgeneralist/PickPlaceCounterToCabinet_pretrain --port 8000
```

```
python -m lerobocasa.launch.simulation_client --policy-port 8000
```

-------
### Explore library of 3200+ objects
View and interact with both human-designed and AI-generated objects. Can also specify the path to a custom mjcf file. If no mjcf path specified, the script will show a random object:
```
python -m robocasa.demos.demo_objects
```
Note: by default this demo shows objaverse objects. To view AI-generated objects, add the flag `--obj_types aigen`.

-------
### Teleoperate the robot
Control the robot directly through the simulation client. Start a policy server (or dummy server), then run simulation client and toggle teleoperation with `t`. Recording is toggled with `Enter`.

Terminal 1:
```
python examples/dummy_policy_server.py --port 8000
```

Terminal 2:
```
python -m lerobocasa.launch.simulation_client --policy-port 8000
```

Note: If using spacemouse in other scripts: you may need to modify `SPACEMOUSE_PRODUCT_ID` in `lerobocasa/macros_private.py`.

## Other useful sections
 - [Overview of Datasets](../datasets/datasets_overview.html)
 - [Overview of Atomic Tasks](../tasks/atomic_tasks.html)
 - [Overview of Composite Tasks](../tasks/composite_tasks.html)
 - [Overview of Scenes](../assets/scenes.html)
 - [Policy Learning Algorithms](../benchmarking/policy_learning_algorithms.html)