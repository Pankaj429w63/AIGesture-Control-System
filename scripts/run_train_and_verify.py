r"""Run training script and verify the saved model exists.

Usage:
  python scripts\run_train_and_verify.py

This will call the training pipeline, wait for it to finish, then check
that the model file exists at the configured `model.save_path`.
"""
import logging
from pathlib import Path
import sys

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_loader import load_config

logger = logging.getLogger("run_train")
logging.basicConfig(level=logging.INFO)


def main():
    cfg = load_config()
    model_path = Path(cfg["model"]["save_path"])

    logger.info("Starting training...")
    try:
        # Import and run the training module programmatically
        from src.training.train import train_and_select
        train_and_select()
    except Exception as e:
        logger.exception("Training failed: %s", e)
        return

    if model_path.exists():
        logger.info("Training completed. Model saved to: %s", model_path)
        print(f"MODEL_OK:{model_path}")
    else:
        logger.error("Training finished but model not found at: %s", model_path)
        print(f"MODEL_MISSING:{model_path}")


if __name__ == '__main__':
    main()
