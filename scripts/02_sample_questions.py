#!/usr/bin/env python3
"""Stratified sampling of questions for evaluation."""
import argparse
from pipeline.config import settings
from pipeline.dataset.loader import download_medqa
from pipeline.dataset.sampler import stratified_sample, save_samples
from pipeline.analysis.img_perspective import tag_img_relevant

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=100, help="Questions per step")
parser.add_argument("--seed", type=int, default=42)
args = parser.parse_args()

if __name__ == "__main__":
    settings.ensure_dirs()
    questions = download_medqa()
    questions = tag_img_relevant(questions)
    samples = stratified_sample(questions, n_per_step=args.n, seed=args.seed)
    save_samples(samples)
    for step, qs in samples.items():
        img_count = sum(1 for q in qs if q.get("img_relevant"))
        print(f"{step}: {len(qs)} questions ({img_count} IMG-relevant)")
