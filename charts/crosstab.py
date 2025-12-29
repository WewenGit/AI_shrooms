import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("agaricus lepiota.csv")

# Afficher les effectifs de target pour chaque modalité de chaque variable du tableau

# vars_tab = [
#     "odor",
#     "gill-size",
#     "gill-color",
#     "stalk-surface-above-ring",
#     "stalk-color-below-ring",
#     "stalk-color-above-ring",
#     "ring-type",
#     "spore-print-color"
# ]

vars_tab = df.columns
vars_tab = [col for col in vars_tab if col != "target"]


for col in vars_tab:
    print(f"\n===== {col} =====")

    counts = pd.crosstab(df[col], df["poisonous"])
    perc = pd.crosstab(df[col], df["poisonous"], normalize="index") * 100

    print(counts)
    print("\n(%)")
    print(perc.round(1))


    plt.figure(figsize=(8, 5))

    if 'e' in counts.columns:
        plt.bar(counts.index, counts['e'], label='edible')
    else:
        counts['e'] = 0
    if 'p' in counts.columns:
        plt.bar(counts.index, counts['p'], bottom=counts['e'], label='poisonous')
    else:
        counts['p'] = 0

    # Add percents above bars
    for i, idx in enumerate(counts.index):
        total = counts.loc[idx].sum()

        txt = ""
        if total > 0:
            pe = perc.loc[idx].get('e', 0)
            pp = perc.loc[idx].get('p', 0)
            txt = f"{pe:.1f}% e\n{pp:.1f}% p"

        plt.text(i, total, txt, ha='center', va='bottom', fontsize=9)

    plt.title(f"Target distribution across the variable '{col}'")
    plt.ylabel("Numbers")
    plt.xlabel(col)
    plt.xticks(rotation=45)
    plt.ylim(0, counts.sum(axis=1).max() * 1.1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"crosstab/crosstab_{col}")
    plt.show()
