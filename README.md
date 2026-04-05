<h1 align="center">RoboCasa</h1>
<!-- ![alt text](https://github.com/UT-Austin-RPL/maple/blob/web/src/overview.png) -->
<img src="docs/images/readme.webp" width="100%" />

**RoboCasa** is a large-scale simulation framework for training generally capable robots to perform everyday tasks. It was [originally released](https://robocasa.ai/assets/robocasa_rss24.pdf) in 2024 by UT Austin researchers. The latest iteration, **RoboCasa365**, builds upon the original release with significant new functionalities to support large-scale training and benchmarking in sim. Four pillars underlie RoboCasa365:
- **Diverse tasks**: 365 tasks created with the guidance of large language models
- **Diverse assets**: including 2,500+ kitchen scenes and 3,200+ 3D objects
- **High-quality demonstrations**: including 600+ hours of human demonstrations in addition to 1,600+ hours of robot datasets created with automated trajectory tools
- **Benchmarking support**: popular policy learning methods including Diffusion Policy, pi, and GR00T


This guide contains information about installation and setup. Please refer to the following resources for additional information:

[**[Home page]**](https://robocasa.ai) &ensp; [**[Documentation]**](https://robocasa.ai/docs/introduction/overview.html) &ensp; [**[RoboCasa365 Paper]**](https://robocasa.ai/assets/robocasa365_iclr26.pdf) &ensp; [**[Original RoboCasa Paper]**](https://robocasa.ai/assets/robocasa_rss24.pdf)

-------
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

### Gym wrapper
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

### Replay recorded datasets (server-client)
Run replay in two terminals using the policy server <-> simulation client flow.

Terminal 1 (start policy server):
```
uv run --with lerobot examples/replay_policy_server.py \
  --dataset_repo_id robotgeneralist/PickPlaceCounterToCabinet_pretrain \
  --port 8000
```

Terminal 2 (start simulation client):
```
uv run python -m lerobocasa.launch.simulation_client \
  --policy-port 8000
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

### Teleoperate the robot
Control the robot directly, either through a keyboard controller or spacemouse. This script renders the robot semi-translucent in order to minimize occlusions and enable better visibility.
```
uv run python -m lerobocasa.demos.demo_teleop
```
Note: If using SpaceMouse, you may need to modify the product ID to your appropriate model, setting `SPACEMOUSE_PRODUCT_ID` in `lerobocasa/macros_private.py`.

-------
## Tasks, datasets, policy learning, and additional use cases
Please refer to the [documentation page](https://robocasa.ai/docs/introduction/overview.html) for information about tasks, datasets, benchmarking, and more.

-------
## Releases
* [2/18/2026] **v1.0**: RoboCasa365 release, with 365 tasks, 2500+ kitchen scenes, 2200+ hours of robot demonstration data, and benchmarking support.
* [10/31/2024] **v0.2**: using RoboSuite `v1.5` as the backend, with improved support for custom robot composition, composite controllers, more teleoperation devices, photo-realistic rendering.

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
