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

This will save raw `.msgpack` recordings.

## Extracting observations
To convert recordings into a LeRobot v3 dataset with rendered videos, run:
```
python -m lerobocasa.converters.convert_recordings_lerobot_v3 \
	--recordings-dir recordings \
	--output-dir /tmp/lerobot_dataset \
	--overwrite
```
This script writes a LeRobot dataset to `--output-dir`.

<div class="admonition note">
<p class="admonition-title">Image resolution</p>

You can override the default image resolution by setting the flags `--camera_height` and `--camera_width`.

</div>

<div class="admonition note">
<p class="admonition-title">Visual randomization</p>

You can add the flag `--generative_textures` to render images with AI-generated environment textures, and `--randomize_cameras` to randomize camera viewpoints for rendering.

</div>

