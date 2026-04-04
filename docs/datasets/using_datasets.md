# Using Datasets

We provide datasets in the lerobot format. There are broadly three types of datasets: **pretraining (human)** datasets, **pretraining (MimicGen)** datasets, and **target (human)** datasets (see [datasets overview](../datasets/datasets_overview.html) for details).

### Downloading datasets

<div class="admonition note">
<p class="admonition-title">Dataset storage location</p>

By default, all datasets are stored under `datasets/` in the root RoboCasa directory. You can change the location for datasets by setting `DATASET_BASE_PATH` in `robocasa/macros_private.py`.

</div>

Here are a few examples to download datasets:

<details>
<summary><b>Click to expand download examples</b></summary>

```
# downloads all datasets
python -m robocasa.scripts.download_datasets --all

# only download pretraining human data
python -m robocasa.scripts.download_datasets --split pretrain --source human

# only download pretraining MimicGen data
python -m robocasa.scripts.download_datasets --split pretrain --source mimicgen

# only download target human data
python -m robocasa.scripts.download_datasets --split target --source human

# download all datasets for specific task(s)
python -m robocasa.scripts.download_datasets --tasks PickPlaceCounterToCabinet ArrangeBreadBasket
```

You can specify `--overwrite` to overwrite existing datasets.
</details>

### Dataset structure
RoboCasa datasets follow the LeRobot format. Here is an overview of important elements of each dataset:

<details>
<summary><b>Click to expand dataset structure</b></summary>

```
lerobot/
├── meta/                               # Metadata files describing the dataset
│   ├── info.json                       # Dataset info (robot type, episodes, frames, fps, features)
│   ├── tasks.jsonl                     # Language instructions with task indices
│   ├── episodes.jsonl                  # Per-episode metadata (index, instruction, length)
│   ├── episodes_stats.jsonl            # Per-episode statistics for actions/proprioception
│   ├── stats.json                      # Aggregated statistics across all episodes
│   ├── modality.json                   # Info contained in observations and action vectors
│   └── embodiment.json                 # Embodiment information
│
├── data/                               # Low-dimensional trajectory data (parquet files)
│   └── chunk-<chunk_id>/
│       └── episode_<episode_id>.parquet   # Proprioception, actions, dones, timestamps
│
├── videos/                             # MP4 video files for each camera view
│   └── chunk-<chunk_id>/
│       ├── observation.images.robot0_agentview_left/
│       │   └── episode_<episode_id>.mp4   # Left third-person camera
│       ├── observation.images.robot0_agentview_right/
│       │   └── episode_<episode_id>.mp4   # Right third-person camera
│       └── observation.images.robot0_eye_in_hand/
│           └── episode_<episode_id>.mp4   # Eye-in-hand camera
│
└── extras/                             # MuJoCo/RoboCasa-specific metadata (non-standard)
    ├── dataset_meta.json               # Environment args and controller configs
    └── episode_<episode_id>/           # Per-episode extras
        ├── ep_meta.json                # Episode metadata (layout, style, fixtures, objects)
        ├── model.xml.gz                # Compressed MJCF MuJoCo model XML
        └── states.npz                  # Raw MuJoCo states for replay (not for training)
```

</details>

### Retrieving dataset metadata
We track each dataset with metadata (paths, task horizon length, etc.) in the [dataset registry](https://github.com/robocasa/robocasa/blob/main/robocasa/utils/dataset_registry.py). You can use the `get_ds_meta()` function to retrieve metadata for a specific task:

```py
from robocasa.utils.dataset_registry import get_ds_meta

ds_meta = get_ds_meta(
    task="PickPlaceCounterToCabinet",
    split="target", # or try "pretrain"
    source="human", # defaults to "human", try "mimicgen" for synthetic data
    demo_fraction=1.0, # the fraction of available demos to use (default is 1.0)
)
```

### Creating environments from dataset metadata
You can initialize a gym environment given the dataset metadata and run random rollouts:
```py
import gymnasium as gym
import robocasa
from robocasa.utils.env_utils import run_random_rollouts

# gather relevant information from ds_meta from previous section
task_name = ds_meta["task"]
split = ds_meta["split"]
horizon = ds_meta["horizon"]

env = gym.make(
    f"robocasa/{task_name}",
    split=split,
    seed=0 # seed environment as needed. set seed=None to run unseeded
)

# run rollouts with random actions and save video
run_random_rollouts(
    env, num_rollouts=3, num_steps=horizon, video_path=f"/tmp/{task_name}_{split}_rollouts.mp4"
)
```

### Creating datasets for training

Here is an example script to access dataset elements:
```py
from lerobot.datasets.lerobot_dataset import LeRobotDataset
import random

# get dataset path from ds_meta from previous section
dataset_path = ds_meta["path"]

ds = LeRobotDataset(repo_id="robocasa365", root=dataset_path)
ep_idx = 5
start = int(ds.episode_data_index["from"][ep_idx]) 
end = int(ds.episode_data_index["to"][ep_idx])
timestep_idx = random.randint(0, end - start)

sample = ds[start + timestep_idx]                                   # Accessing a random sample from the 5th demo in the dataset
right_img = sample["observation.images.robot0_agentview_right"]     # Accessing the right camera image
action = sample["action"]                                           # Accessing the action taken    
instruction = sample["task"]                                        # Accessing the instruction for the episode
```

### Training beyond a single dataset

The code above returns meta data for a single dataset. You can retrieve information for a collection of datasets using the `get_ds_soup()` function, which returns a list of dataset metadata:

```py
from robocasa.utils.dataset_registry import get_ds_soup

ds_soup = get_ds_soup(
    task_soup="atomic_seen", # the list of tasks
    split="target", # or try "pretrain"
    source="human", # defaults to "human", try "mimicgen" for synthetic data
    demo_fraction=1.0, # the fraction of available demos to use (default is 1.0)
)
```

Prominent dataset soups are registerd in [the dataset soup registry](https://github.com/robocasa/robocasa/blob/main/robocasa/utils/dataset_registry.py).



### Inspecting and visualizing datasets

To get dataset statistics (filter keys, objects, task language, scenes):
```
python robocasa/scripts/get_dataset_info.py --dataset <ds-path>
```

You can visualize dataset videos by looking at the `videos` folder under each lerobot dataset directory. To visualize a dataset and save a video:
```
python robocasa/scripts/playback_dataset.py --n 10 --dataset <ds-path>
```
This will save a video of 10 random demonstrations in the same path as the dataset. You can play the full dataset by removing the `--n` flag.