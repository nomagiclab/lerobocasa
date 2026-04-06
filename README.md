## Installation
`LeRoboCasa` is a forked version of [`RoboCasa`](https://robocasa.ai),
maintained with a devcontainer-first workflow.
The container provisions the right system dependencies,
runs `uv sync`, and configures macros automatically.

### Python version requirement
This repository now targets Python `3.12`.
If you are refreshing an existing local environment, run:

```sh
uv python install 3.12
uv venv --python 3.12 --clear
uv lock
uv sync
```

### Dev Container Setup

You have to install docker to be able to use the container setup.

#### Option A: VS Code Dev Containers
1. Open this repository in VS Code.
2. Run the command `Dev Containers: Reopen in Container`.
3. Wait for container setup to complete (`.devcontainer/post-create.sh` runs automatically).
4. Open the integrated terminal to enter the container shell.

#### Option B: Devcontainer CLI
Build and start the container from the repository root:

```sh
devcontainer up --remove-existing-container --workspace-folder .
```

Run:

```sh
devcontainer exec --workspace-folder . -- bash -l
```

to enter the container shell.

### Lite display in browser (desktop-lite / noVNC)
The devcontainer exposes a browser desktop at port `6080`.

1. Open `http://localhost:6080` in your browser.
2. If you are using VS Code, you can also open the forwarded `6080` port from the Ports panel.

Use Chrome, Edge, or Firefox. Safari is not supported for this display workflow.

### Veryfing the installation

After the container is up, you can run demos with:

```sh
uv run python -m lerobocasa.demos.demo_kitchen_scenes
```

After selecting options in the terminal,
a window with a scene should pop up on the desktop in the web browser.

### Asset setup
If you need to force setup steps manually inside the container:

```sh
uv run python -m lerobocasa.scripts.setup_macros
uv run python -m lerobocasa.scripts.download_kitchen_assets
```

-------
## Basic Usage

### Simulation Node

You can start a simulation node with:

```
uv run python -m lerobocasa.launch.simulation_node \
  --policy-port 8000
```

The policy port flag allows you to connect to the node with some policy server later on.

### Replay Recorded Datasets
Assuming that you have a simulation node running,
you can replay a lerobot v3.0 dataset
by starting the example replay policy server in another shell:

```
uv run --with lerobot examples/replay_policy_server.py \
  --dataset_repo_id robotgeneralist/PickPlaceCounterToCabinet_pretrain \
  --port 8000
```

If the replay crashes without any explicit error, try rebuilding the container.
Sometimes OOM errors are thrown. Not sure why.

### Evaluating Policies

First try at training and evaluating models can be found on
[this branch](https://github.com/nomagiclab/openpi/tree/156-robocasa-integration)
in our internal `openpi` repo.
If the policy server is running inside a devcontainer on a remote machine,
remember to properly forward appropriate ports, e.g., for jerryrig:

```bash
ssh -N -L 0.0.0.0:18000:127.0.0.1:8000 jerryrig
```

Then the simulation node can be run with:

```bash
uv run python -m lerobocasa.launch.simulation_node --policy-host host.docker.internal --policy-port 18000
```

The policy does random movements on a 5k checkpoint,
so I suspect bugs are present.
But at least on a general communication level the setup is working.

### Teleoperate and Record with a Simulation Node
Inside the simulation node, you can teleoperate the robot and record new trajectories.
Press:
 - `t` to toggle teleoperation,
 - `Enter` to start / stop recording,
 - `p` to connect or disconnect from a policy server.

Note: If using SpaceMouse elsewhere, you may need to modify `SPACEMOUSE_PRODUCT_ID` in `lerobocasa/macros_private.py`.

If you want to verify the recordings, 
you can replay raw recordings using the `replay_recording_server.py`:

```
uv run --with lerobot examples/replay_recording_server.py \
  --recordings_dir recordings \
  --port 8000
```

To convert the recordings into a lerobot v3.0 dataset and upload to HF:

```
uv run python -m lerobocasa.converters.convert_recordings_lerobot_v3 \
    --recordings-dir recordings \
    --output-dir /tmp/pickplace_target_v3 \
    --upload-repo-id robotgeneralist/lerobocasa_custom_recordings \
    --overwrite
```

### Explore kitchen scenes
Explore 2500+ kitchen scenes:
```
uv run python -m lerobocasa.demos.demo_kitchen_scenes
```

### Explore library of 2500+ objects
View and interact with both human-designed and AI-generated objects:
```
uv run python -m lerobocasa.demos.demo_objects
```
Note: By default, this demo shows objaverse objects. To view AI-generated objects, add the flag `--obj_types aigen`.

-------

### Gym wrapper
THIS IS PART OF THE ORIGINAL ROBOCASA REPO.
HAVEN'T YET VERIFIED IF THE THING BELOW WORKS

You can create environments using gym wrappers and run rollouts:
```py
import gymnasium as gym
import lerobocasa
from lerobocasa.utils.env_utils import run_random_rollouts

env = gym.make(
   "lerobocasa/PickPlaceCounterToCabinet",
    split="pretrain", # use 'pretrain' or 'target' kitchen scenes and objects
    seed=0 # seed environment as needed. set seed=None to run unseeded
)

# run rollouts with random actions and save video
run_random_rollouts(
    env, num_rollouts=3, num_steps=100, video_path="/tmp/test.mp4"
)
```

-------
## License
Code: [MIT License](https://opensource.org/license/mit)

Assets and Datasets: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en)
 
-------
## Citation

**RoboCasa365:**

```bibtex
@inproceedings{robocasa365,
  title={RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots},
  author={Soroush Nasiriany and Sepehr Nasiriany and Abhiram Maddukuri and Yuke Zhu},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2026}
}
```

**RoboCasa (Original Release):**

```bibtex
@inproceedings{robocasa2024,
  title={RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots},
  author={Soroush Nasiriany and Abhiram Maddukuri and Lance Zhang and Adeet Parikh and Aaron Lo and Abhishek Joshi and Ajay Mandlekar and Yuke Zhu},
  booktitle={Robotics: Science and Systems (RSS)},
  year={2024}
}
