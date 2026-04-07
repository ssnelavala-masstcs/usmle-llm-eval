"""matplotlib/seaborn plot helpers for paper figures."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

FIGURES_DIR = Path("evaluation/figures")

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("colorblind")


def accuracy_bar_chart(acc_df: pd.DataFrame, output_path: Path = None) -> Path:
    """Horizontal bar chart of model accuracy with 95% CI error bars."""
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("colorblind", len(acc_df))
    ax.barh(
        acc_df["group"],
        acc_df["accuracy"],
        xerr=[
            acc_df["accuracy"] - acc_df["ci_lower"],
            acc_df["ci_upper"] - acc_df["accuracy"],
        ],
        capsize=4,
        color=colors,
    )
    ax.set_xlabel("Accuracy (with 95% CI)", fontsize=12)
    ax.set_title("LLM Accuracy on USMLE-Style Questions", fontsize=14, fontweight="bold")
    ax.axvline(x=0.6, color="red", linestyle="--", alpha=0.5, label="Passing threshold (60%)")
    ax.legend()
    plt.tight_layout()
    out = output_path or FIGURES_DIR / "fig1_accuracy_by_model.pdf"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    return out


def subject_heatmap(pivot_df: pd.DataFrame, output_path: Path = None) -> Path:
    """Heatmap of model × subject accuracy."""
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(
        pivot_df,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        vmin=0,
        vmax=1,
        ax=ax,
        linewidths=0.5,
    )
    ax.set_title("Model Accuracy by Medical Subject", fontsize=14, fontweight="bold")
    ax.set_xlabel("Subject", fontsize=11)
    ax.set_ylabel("Model", fontsize=11)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out = output_path or FIGURES_DIR / "fig2_subject_heatmap.pdf"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    return out


def img_gap_bar_chart(img_df: pd.DataFrame, output_path: Path = None) -> Path:
    """Grouped bar chart: IMG-relevant vs. non-IMG accuracy per model."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(img_df))
    ax.bar([i - 0.2 for i in x], img_df["img_accuracy"], width=0.4, label="IMG-relevant Qs", alpha=0.8)
    ax.bar([i + 0.2 for i in x], img_df["non_img_accuracy"], width=0.4, label="Non-IMG Qs", alpha=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(img_df["model"], rotation=45, ha="right")
    ax.set_ylabel("Accuracy")
    ax.set_title("Model Accuracy: IMG-Relevant vs. Non-IMG Questions")
    ax.legend()
    plt.tight_layout()
    out = output_path or FIGURES_DIR / "fig3_img_gap.pdf"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    return out
