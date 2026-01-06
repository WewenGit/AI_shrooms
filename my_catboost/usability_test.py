import pandas as pd
from my_catboost import CatBoostClassifier


## Test d'utilisation du modèle CatBoost stocké dans le fichier .cbm

# Model
model_cb = CatBoostClassifier()
model_cb.load_model("cb_model.cbm")

# New observation (mushroom)
new_data = pd.DataFrame([{
    "cap-shape": "x",
    "cap-surface": "s",
    "cap-color": "n",
    "bruises": "t",
    "odor": "p",
    "gill-attachment": "f",
    "gill-spacing": "c",
    "gill-size": "n",
    "gill-color": "k",
    "stalk-shape": "e",
    "stalk-root": "e",
    "stalk-surface-above-ring": "s",
    "stalk-surface-below-ring": "s",
    "stalk-color-above-ring": "w",
    "stalk-color-below-ring": "w",
    "veil-color": "w",
    "ring-number": "o",
    "ring-type": "p",
    "spore-print-color": "k",
    "population": "s",
    "habitat": "u"
}])

# Prédiction
pred = model_cb.predict(new_data)
proba = model_cb.predict_proba(new_data)

print("Predicted class :", pred[0])
print("Probabilities  :", proba[0])
