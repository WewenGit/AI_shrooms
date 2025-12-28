import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib

data = pd.read_csv("../mushroom/agaricus lepiota.csv")
target = "poisonous"


## Infos
print(data[target].value_counts())
print(data.info())
#print(data.describe())
print()


## Get X and y
y = data[target]
X = data.drop(target, axis = 1)


## One-hot encoding of X
hotEncoder = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
Xhot = hotEncoder.fit_transform(X)

Xhot = pd.DataFrame(
    Xhot,
    columns=hotEncoder.get_feature_names_out()
)

# Explain why one-hot encoding and not label encoding
# https://www.geeksforgeeks.org/machine-learning/one-hot-encoding-vs-label-encoding/


## Split data
x_train, x_test, y_train, y_test  = train_test_split(Xhot, y, test_size=0.25, random_state=42)


## Model
model_rf = RandomForestClassifier(
    n_estimators=100,               # nb arbres dans forêt
    criterion='gini',               # critère pour construire les arbres (séparer les branches)
    max_depth=None,                 # profondeur maximale des arbres
    min_samples_split=2,            # nb échantillons min dans feuille pour faire séparation
    min_samples_leaf=1,             # nb échantillons minimal pour créer feuille
    min_weight_fraction_leaf=0.0,   # nb total échantillon min pour créer une feuille
    max_features='sqrt',            # nb colonnes sélectionnées pour chaque arbre
    max_leaf_nodes=None,            # nb max feuilles
    min_impurity_decrease=0.0,      # baisse min critère d’impureté pour faire séparation
    bootstrap=True,                 # pour utiliser du bootstrap, si False -> même échantillon pour chaque arbre
    oob_score=False,                #
    n_jobs=None,                    # nb traitements à effectuer en parallèle
    random_state=None,              # graine aléatoire
    verbose=0,                      #
    warm_start=False,               # repartir du résultat du dernier apprentissage pour faire l’apprentissage
    class_weight=None,              # poids associés à chaque classe
    ccp_alpha=0.0,                  #
    max_samples=None,               # pour réduire nb observations dans échantillons bootstrap
)


## Learning
model_rf.fit(x_train, y_train)


## Importances of variables

# Importances calculées par modalité à cause du one-hot encoding
importance = model_rf.feature_importances_
feature_names = Xhot.columns
feature_importance = pd.Series(importance, index=feature_names)

# Importances par variable d'origine en faisant les sommes des importances par modalités
# Somme plus cohérente que moyenne pour Random Forest : importance globale de la variable = contribution totale
original_features = feature_importance.index.str.split("_").str[0]
fi_grouped = feature_importance.groupby(original_features).sum()
fi_grouped = fi_grouped.sort_values(ascending=False)

print("------ Importances ------")
print(fi_grouped)


## Testing

print(f"------------------------------------------------------------")

predict = model_rf.predict(x_test)

accuracy = accuracy_score(y_test, predict)
print(f"Accuracy : {accuracy*100} %\n")

confusion_matrix = pd.DataFrame(
    confusion_matrix(y_test, predict),
    index = ["edible_data", "poisonous_data"],
    columns = ["edible_predict", "poisonous_predict"]
)

print(confusion_matrix)

print(f"------------------------------------------------------------")


## Production : Export model with pipeline

pipeline = Pipeline(steps=[
    ("encoder", hotEncoder),
    ("model", model_rf)
])

pipeline.fit(X, y)

joblib.dump(pipeline, "rf_pipeline.pkl")
