import joblib
import pandas as pd

## Test d'utilisation du modèle Random Forest stocké dans le fichier .pkl

# Import pipeline (model + encoder)
pipeline = joblib.load("rf_pipeline.pkl")

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
    "veil-type": "p",
    "veil-color": "w",
    "ring-number": "o",
    "ring-type": "p",
    "spore-print-color": "k",
    "population": "s",
    "habitat": "u"
}])

# Prédiction
pred = pipeline.predict(new_data)
proba = pipeline.predict_proba(new_data)

print("Predicted class :", pred[0])
print("Probabilities  :", proba[0])
