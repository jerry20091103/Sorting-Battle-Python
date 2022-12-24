# Sorting-Battle-Python
[![Python application](https://github.com/jerry20091103/Sorting-Battle-Python/actions/workflows/python-app.yml/badge.svg)](https://github.com/jerry20091103/Sorting-Battle-Python/actions/workflows/python-app.yml)

The 1P and 2P training models for Sorting Battle the game.
If you can't use cuda, please go to `training/training_model.py` to change related code.
To adjust model hyperparameters, please go to `training/training_model.py`.
To adjust training hyperparameters, please go to `training/train_1P.py` or `training/train_2P.py`.

## Prerequisite
```
pip install torch
pip install onnx
```

## Usage
```
cd training
python train_1P.py
python train_2P.py
```
