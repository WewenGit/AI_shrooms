import pandas as pd
import catboost as cb
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
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


## Identify categorical columns
cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

# normally all of columns are categorical
assert len(cat_features) == len(X.columns)

# Advantage: CatBoost manages categorical columns automatically


## Split data
x_train, x_test, y_train, y_test  = train_test_split(X, y, test_size=0.25, random_state=42)


## Model
model_cb = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.02,
    depth=6,
    silent=True,
    #verbose=200,
    random_seed=42
)

## Learning
model_cb.fit(x_train, y_train, cat_features=cat_features)


## Importances of variables
importance = model_cb.feature_importances_
feature_names = X.columns
feature_importance = pd.Series(importance, index=feature_names).sort_values(ascending=False)

print("------ Importances ------")
print(feature_importance)


## Testing

print(f"------------------------------------------------------------")

predict = model_cb.predict(x_test)

accuracy = accuracy_score(y_test, predict)
print(f"Accuracy : {accuracy*100} %\n")

confusion_matrix = pd.DataFrame(
    confusion_matrix(y_test, predict),
    index = ["edible_data", "poisonous_data"],
    columns = ["edible_predict", "poisonous_predict"]
)

print(confusion_matrix)

print(f"------------------------------------------------------------")


## Production : Export model
model_cb.save_model("cb_model.cbm")
