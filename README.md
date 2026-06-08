# AI-Powered Touchless Multimedia and Workspace Control System

Real-time hand gesture recognition system that controls multimedia and workspace operations using MediaPipe, OpenCV, and machine learning.

Features
- Real-time gesture recognition (multi-hand)
- Face authentication before control activation
- Custom gesture registration and dataset collection
- Training and evaluation pipeline with model comparison
- Real-time inference and system controls (volume, brightness, media)
- Logging, configuration, and modular architecture

See `config/config.yaml` for configurable mappings and thresholds.

Getting started
1. Create a virtual environment with Python 3.11+
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Prepare dataset in `dataset/` or collect using `src/dataset_collection/collect_data.py`.
4. Train models: `python -m src.training.train`
5. Run real-time demo: `python main.py`

Project structure: see the project root for a full tree.