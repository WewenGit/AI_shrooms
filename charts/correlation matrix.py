import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

# --- Fonction pour le V de Cramér ---
def cramers_v(x, y):
    # Table de contingence
    confusion_matrix = pd.crosstab(x, y)
    # Si la matrice est vide ou si une dimension vaut 1 → pas de variation
    if confusion_matrix.shape[0] < 2 or confusion_matrix.shape[1] < 2:
        return np.nan
    chi2, p, dof, expected = chi2_contingency(confusion_matrix)
    n = confusion_matrix.sum().sum()
    # Correction pour éviter division par zéro
    denom = n * (min(confusion_matrix.shape) - 1)
    if denom == 0:
        return np.nan
    v = np.sqrt(chi2 / denom)
    # Par sécurité (évite warnings si chi2 négatif par erreur numérique)
    if np.isnan(v) or np.isinf(v):
        return np.nan
    return v

# --- Charger le dataset ---
df = pd.read_csv("agaricus lepiota.csv")

# --- Sélection des variables catégorielles (facultatif si toutes le sont) ---
cat_cols = df.select_dtypes(include=['object', 'category']).columns

# --- Calcul de la matrice V de Cramér ---
matrix = np.zeros((len(cat_cols), len(cat_cols)))

for i, col1 in enumerate(cat_cols):
    for j, col2 in enumerate(cat_cols):
        matrix[i, j] = cramers_v(df[col1], df[col2])

# Convertir en DataFrame pour affichage
cramer_df = pd.DataFrame(matrix, index=cat_cols, columns=cat_cols)

# --- Heatmap ---
plt.figure(figsize=(10, 8))
sns.heatmap(cramer_df, annot=True, cmap="coolwarm", vmin=0, vmax=1)
plt.title("Matrice du V de Cramér (corrélation entre variables catégorielles)")
#plt.savefig("v_cramer_matrix.png")
plt.show()