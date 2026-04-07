#!/usr/bin/env python3
"""Export results as LaTeX tables for the paper."""
import pandas as pd
from pathlib import Path
from pipeline.config import settings

RESULTS_DIR = settings.results_dir
PAPER_DIR = Path("paper")


def df_to_latex(df: pd.DataFrame, caption: str, label: str) -> str:
    latex = df.to_latex(index=False, float_format="%.3f", booktabs=True)
    return f"""\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
{latex}
\\end{{table}}
"""


if __name__ == "__main__":
    for csv_file in RESULTS_DIR.glob("*.csv"):
        df = pd.read_csv(csv_file)
        table_name = csv_file.stem
        caption = table_name.replace("_", " ").title()
        label = f"tab:{table_name}"
        latex_str = df_to_latex(df, caption, label)
        out = PAPER_DIR / "sections" / f"table_{table_name}.tex"
        out.write_text(latex_str)
        print(f"Exported: {out}")
