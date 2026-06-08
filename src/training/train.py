"""Train and compare multiple classifiers, save best model."""
from pathlib import Path
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from src.utils.config_loader import load_config
from src.preprocessing.preprocess import load_dataset, split_features_labels, standardize
from src.utils.logger import setup_logger

def train_and_select(path: str = None):
    cfg = load_config()
    logger = setup_logger("train", cfg.get("logging", {}).get("file"))
    data_path = path or cfg["dataset"]["path"]
    df = load_dataset(data_path)
    X, y = split_features_labels(df, cfg["model"]["label_col"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=cfg["model"]["random_state"], stratify=y)
    X_train_s, X_test_s, scaler = standardize(X_train, X_test)

    models = {
        "RandomForest": RandomForestClassifier(random_state=cfg["model"]["random_state"]),
        "SVM": SVC(probability=True, random_state=cfg["model"]["random_state"]),
        "KNN": KNeighborsClassifier(),
        "MLP": MLPClassifier(max_iter=500, random_state=cfg["model"]["random_state"])
    }

    results = {}
    for name, m in models.items():
        logger.info(f"Training {name}...")
        m.fit(X_train_s, y_train)
        ypred = m.predict(X_test_s)
        acc = accuracy_score(y_test, ypred)
        p, r, f, _ = precision_recall_fscore_support(y_test, ypred, average='weighted', zero_division=0)
        results[name] = {"model": m, "accuracy": acc, "precision": p, "recall": r, "f1": f}
        logger.info(f"{name} - Acc: {acc:.4f} F1: {f:.4f}")

    # select best by f1
    best_name = max(results.keys(), key=lambda k: results[k]["f1"])
    best = results[best_name]["model"]
    logger.info(f"Best model: {best_name}")

    # save model, scaler
    Path(cfg["model"]["metrics_path"]).mkdir(parents=True, exist_ok=True)
    model_out = cfg["model"]["save_path"]
    Path(model_out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": best, "scaler": scaler}, model_out)
    logger.info(f"Saved best model to {model_out}")

    # plot confusion matrix for best
    ypred_best = best.predict(X_test_s)
    cm = confusion_matrix(y_test, ypred_best, labels=best.classes_)
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=best.classes_, yticklabels=best.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'Confusion Matrix - {best_name}')
    plt.tight_layout()
    plt.savefig(Path(cfg["model"]["metrics_path"]) / "confusion_matrix.png")

    return results, best_name

if __name__ == "__main__":
    train_and_select()
