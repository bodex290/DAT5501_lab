#!/usr/bin/env python3
# bike_tree.py
# Decision Tree mini-project on the Bike Sharing (daily) dataset.
# Usage:
#   python bike_tree.py --csv day.csv --max-depth 4 --tune-depth
# Outputs are saved into ./outputs/

import argparse
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_recall_fscore_support,
)

def parse_args():
    p = argparse.ArgumentParser(description="Decision Tree on Bike Sharing (daily) data")
    p.add_argument("--csv", default="day.csv", help="Path to day.csv")
    p.add_argument("--test-size", type=float, default=0.30, help="Test split size (0-1)")
    p.add_argument("--random-state", type=int, default=42, help="Random seed")
    p.add_argument("--max-depth", type=int, default=4, help="Tree max depth (None for unlimited)")
    p.add_argument("--threshold-quantile", type=float, default=0.5,
                   help="Quantile for High/Low demand threshold (default=0.5 median)")
    p.add_argument("--tune-depth", action="store_true",
                   help="If set, evaluates depths 1..15 and saves a tuning plot")
    return p.parse_args()

def load_and_prepare(csv_path: str, q: float):
    df = pd.read_csv(csv_path)

    # Create binary target: High(1) if cnt > quantile threshold else Low(0)
    thresh = df["cnt"].quantile(q)
    df["high_demand"] = (df["cnt"] > thresh).astype(int)

    # Columns present in day.csv
    drop_if_exist = ["instant", "dteday", "casual", "registered", "cnt"]
    for c in drop_if_exist:
        if c in df.columns:
            df.drop(columns=c, inplace=True)

    y = df["high_demand"]
    X = df.drop(columns=["high_demand"])

    # Categorical (treated as categories even if encoded as ints)
    cat_cols = [c for c in ["season", "yr", "mnth", "holiday", "weekday",
                            "workingday", "weathersit", "hr"] if c in X.columns]
    num_cols = [c for c in X.columns if c not in cat_cols]

    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )
    return X, y, pre, cat_cols, num_cols

def feature_names_from(preprocessor, cat_cols, num_cols):
    ohe = preprocessor.named_transformers_["cat"]
    cat_names = []
    if cat_cols:
        cat_names = list(ohe.get_feature_names_out(cat_cols))
    return cat_names + num_cols

def ensure_outdir():
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    return out

def train_and_report(X, y, pre, max_depth, test_size, rs, outdir):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=test_size,
                                          random_state=rs, stratify=y)
    clf = Pipeline(
        steps=[
            ("pre", pre),
            ("tree", DecisionTreeClassifier(max_depth=max_depth, random_state=rs)),
        ]
    )
    clf.fit(Xtr, ytr)
    yhat = clf.predict(Xte)

    print("\n=== Classification Report (test) ===")
    print(classification_report(yte, yhat, target_names=["Low", "High"], digits=3))

    # Confusion matrix
    fig = plt.figure()
    ConfusionMatrixDisplay.from_estimator(clf, Xte, yte)
    plt.title("Confusion Matrix")
    fig.savefig(outdir / "confusion_matrix.png", bbox_inches="tight")
    plt.close(fig)

    # Extract feature importances with correct names
    # Fit a fresh preprocessor to learn categories; then get names
    pre_fitted = clf.named_steps["pre"]
    feat_names = feature_names_from(pre_fitted, 
                                    pre_fitted.transformers_[0][2],  # discovered cat cols
                                    pre_fitted.transformers_[1][2])  # discovered num cols
    importances = clf.named_steps["tree"].feature_importances_

    # Plot top 15 importances
    idx = np.argsort(importances)[::-1]
    top = min(15, len(idx))
    fig = plt.figure(figsize=(8, 5))
    plt.bar(range(top), importances[idx][:top])
    plt.xticks(range(top), [feat_names[i] for i in idx[:top]], rotation=60, ha="right")
    plt.ylabel("Importance")
    plt.title("Top Feature Importances")
    fig.savefig(outdir / "feature_importances.png", bbox_inches="tight")
    plt.close(fig)

    # Plot the tree (on transformed features)
    # We need the fully transformed training set and names
    Xt = pre_fitted.transform(Xtr)
    tree_model = clf.named_steps["tree"]
    fig = plt.figure(figsize=(18, 10))
    plot_tree(
        tree_model,
        feature_names=feat_names,
        class_names=["Low", "High"],
        filled=True,
        rounded=True,
        impurity=True,
        proportion=True,
    )
    plt.title(f"Decision Tree (max_depth={tree_model.get_params().get('max_depth')})")
    fig.savefig(outdir / "decision_tree.png", bbox_inches="tight")
    plt.close(fig)

    return clf, (Xtr, Xte, ytr, yte)

def depth_tuning(X, y, pre, rs, outdir):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30,
                                          random_state=rs, stratify=y)
    depths = list(range(1, 16))
    rows = []
    for d in depths:
        pipe = Pipeline(
            steps=[("pre", pre),
                   ("tree", DecisionTreeClassifier(max_depth=d, random_state=rs))]
        )
        pipe.fit(Xtr, ytr)
        yhat = pipe.predict(Xte)
        p, r, f1, _ = precision_recall_fscore_support(yte, yhat, average="binary", zero_division=0)
        rows.append({"depth": d, "precision": p, "recall": r, "f1": f1})

    df = pd.DataFrame(rows)
    df.to_csv(outdir / "depth_tuning.csv", index=False)

    # Plot metrics vs depth
    fig = plt.figure(figsize=(7, 5))
    plt.plot(df["depth"], df["precision"], marker="o", label="Precision")
    plt.plot(df["depth"], df["recall"], marker="o", label="Recall")
    plt.plot(df["depth"], df["f1"], marker="o", label="F1")
    plt.xlabel("Tree Depth")
    plt.ylabel("Score")
    plt.title("Precision/Recall/F1 vs Tree Depth")
    plt.legend()
    fig.savefig(outdir / "depth_tuning.png", bbox_inches="tight")
    plt.close(fig)

    print("\nSaved depth tuning metrics to outputs/depth_tuning.csv and outputs/depth_tuning.png")
    best = df.sort_values("f1", ascending=False).iloc[0]
    print(f"Best depth by F1: {int(best['depth'])}  (F1={best['f1']:.3f}, "
          f"Precision={best['precision']:.3f}, Recall={best['recall']:.3f})")

def main():
    args = parse_args()
    outdir = ensure_outdir()

    print("Loading data...")
    X, y, pre, _, _ = load_and_prepare(args.csv, args.threshold_quantile)

    print(f"Records: {len(X)}. Positive class rate: {y.mean():.3f}")
    print("Training model...")
    _clf, _splits = train_and_report(
        X, y, pre, args.max_depth, args.test_size, args.random_state, outdir
    )

    if args.tune_depth:
        print("Running depth tuning (1..15)...")
        # Important: clone a fresh preprocessor for tuning to avoid leakage of fitted state
        pre2 = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                 [c for c in ["season","yr","mnth","holiday","weekday","workingday","weathersit","hr"] if c in X.columns]),
                ("num", "passthrough",
                 [c for c in X.columns if c not in ["season","yr","mnth","holiday","weekday","workingday","weathersit","hr"]]),
            ]
        )
        depth_tuning(X, y, pre2, args.random_state, outdir)

    print("\nDone. Saved figures to ./outputs/:")
    print(" - confusion_matrix.png")
    print(" - feature_importances.png")
    print(" - decision_tree.png")
    if args.tune_depth:
        print(" - depth_tuning.csv")
        print(" - depth_tuning.png")

if __name__ == "__main__":
    main()