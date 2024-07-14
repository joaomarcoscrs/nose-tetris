# nose tetris 👃🧱🎮

A Tetris-like game, but instead of using your keys to play you use your nose movements, processed through a computer vision Keypoint Detection model.

100% Open Source, built using [Inference](https://github.com/roboflow/inference) and [Pygame](https://github.com/pygame/pygame). The computer vision project is also open source, you can check it and test on [Universe](https://universe.roboflow.com/my-workspace-vqpvh/facial-features-keypoints/model).

## the game 🎮

The controls are:
- Tilt your nose left: shape goes left
- Tilt your nose right: shape goes right
- Tilt your nose up: shape rotates
- Tilt your nose down: shape accelerates the descend

## system overview 💻

![system overview](excalidraw.png)

## run 🧑‍💻

You will need to use a Python>=3.8,<=3.11 environment.

```bash
export ROBOFLOW_API_KEY=<your_roboflow_api_key>

pip install -r requirements.txt

python run.py
```

It will start your game and wait until your system is receiving predictions to start playing.

The first time you run, you may need to authorize your terminal to open your camera. If that happens it will break, authorize it and run again.

## next steps 🚀

- [ ] Multiplayer mode
