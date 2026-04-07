#!/usr/bin/env python3
"""Generate all figures for the paper."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from pipeline.config import settings

FIGURES_DIR = Path("evaluation/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("colorblind")

if __name__ == "__main__":
    results_dir = settings.results_dir

    # Figure 1: Accuracy by model (bar chart with CI)
    acc_file = results_dir / "accuracy_by_model.csv"
    if acc_file.exists():
        df = pd.read_csv(acc_file)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(
            df["group"],
            df["accuracy"],
            xerr=[df["accuracy"] - df["ci_lower"], df["ci_upper"] - df["accuracy"]],
            capsize=4,
            color=sns.color_palette("colorblind", len(df)),
        )
        ax.set_xlabel("Accuracy (with 95% CI)", fontsize=12)
        ax.set_title("LLM Accuracy on USMLE-Style Questions", fontsize=14, fontweight="bold")
        ax.axvline(x=0.6, color="red", linestyle="--", alpha=0.5, label="Passing threshold (60%)")
        ax.legend()
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "fig1_accuracy_by_model.pdf", dpi=300, bbox_inches="tight")
        plt.savefig(FIGURES_DIR / "fig1_accuracy_by_model.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("Saved Fig 1: accuracy by model")
    else:
        print("Skipping Fig 1: accuracy_by_model.csv not found. Run 04_run_analysis.py first.")

    # Figure 2: Subject heatmap (requires merged model×subject pivot)
    print("Figure 2 (heatmap) requires merged results — run after full evaluation.")

    # Figure 3: IMG gap analysis
    img_file = results_dir / "img_gap_analysis.csv"
    if img_file.exists():
        df = pd.read_csv(img_file)
        fig, ax = plt.subplots(figsize=(8, 5))
        x = range(len(df))
        ax.bar([i - 0.2 for i in x], df["img_accuracy"], width=0.4, label="IMG-relevant Qs", alpha=0.8)
        ax.bar([i + 0.2 for i in x], df["non_img_accuracy"], width=0.4, label="Non-IMG Qs", alpha=0.8)
        ax.set_xticks(list(x))
        ax.set_xticklabels(df["model"], rotation=45, ha="right")
        ax.set_ylabel("Accuracy")
        ax.set_title("Model Accuracy: IMG-Relevant vs. Non-IMG Questions")
        ax.legend()
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "fig3_img_gap.pdf", dpi=300, bbox_inches="tight")
        plt.savefig(FIGURES_DIR / "fig3_img_gap.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("Saved Fig 3: IMG gap analysis")
    else:
        print("Skipping Fig 3: img_gap_analysis.csv not found. Run 04_run_analysis.py first.")
