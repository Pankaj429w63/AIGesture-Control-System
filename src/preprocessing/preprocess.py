import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple

def load_dataset(path: str) -> pd.DataFrame:
    # read with skipinitialspace to handle CSVs with spaces after commas
    df = pd.read_csv(path, skipinitialspace=True)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    return df

def split_features_labels(df: pd.DataFrame, label_col: str = "label") -> Tuple[np.ndarray, np.ndarray]:
    X = df.drop(columns=[label_col]).values
    y = df[label_col].values
    return X, y

def standardize(X_train: np.ndarray, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    return X_train_s, X_test_s, scaler

def augment_noise(X: np.ndarray, sigma: float = 0.01, factor: int = 2) -> np.ndarray:
    res = [X]
    for _ in range(factor-1):
        noise = np.random.normal(0, sigma, X.shape)
        res.append(X + noise)
    return np.vstack(res)
