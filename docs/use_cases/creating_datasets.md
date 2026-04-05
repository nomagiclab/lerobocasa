# Creating Datasets

## Collecting human demonstrations
Use the simulation client recording workflow:

Terminal:
```
python -m lerobocasa.launch.simulation_node --policy-port 8000
```

<div class="admonition note">
<p class="admonition-title">Attention Mac users</p>

Mac users must prepend this script with `mj`, ie. `mjpython`

</div>

In the simulation node, press `t` to toggle teleoperation and press `Enter` to start / stop recording. Press `p` to connect or disconnect from a policy server.

This saves raw `.msgpack` recordings in `recordings/`.

## Extracting observations
To convert recordings into a [LeRobot](https://github.com/huggingface/lerobot) v3 dataset with rendered videos, run:
```
python -m lerobocasa.converters.convert_recordings_lerobot_v3 \
	--recordings-dir recordings \
	--output-dir /tmp/lerobot_dataset \
	--overwrite
```
For more information on the generated dataset structure, please refer to the [Using Datasets](../datasets/using_datasets.md) guide.

<div class="admonition note">
<p class="admonition-title">Image resolution</p>

You can override the default image resolution by setting the flags `--camera_height` and `--camera_width`.

</div>
