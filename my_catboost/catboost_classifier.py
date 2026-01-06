import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


class CatBoostAnalyzer():
    
    def __init__(self):
        self.data = pd.read_csv("./mushroom/agaricus_lepiota.csv")
        self.target = "poisonous"


        ## Data cleaning
        self.data = self.data.drop(columns=["veil-type"])

        self.text = ""
        ## Infos
        self.text+=str(self.data[self.target].value_counts())+"\n"
        #print(data.describe())


        ## Get X and y
        self.y = self.data[self.target]
        self.X = self.data.drop(self.target, axis = 1)


        ## Identify categorical columns
        self.cat_features = self.X.select_dtypes(include=['object', 'category']).columns.tolist()

        # normally all of columns are categorical
        assert len(self.cat_features) == len(self.X.columns)

        # Advantage: CatBoost manages categorical columns automatically


        ## Split data
        self.x_train, self.x_test, self.y_train, self.y_test  = train_test_split(self.X, self.y, test_size=0.25, random_state=42)


        ## Model
        self.model_cb = CatBoostClassifier(
            iterations=1000,
            learning_rate=0.02,
            depth=6,
            silent=True,
            #verbose=200,
            random_seed=42
        )

        ## Learning
        self.model_cb.fit(self.x_train, self.y_train, cat_features=self.cat_features)


        ## Importances of variables
        self.importance = self.model_cb.feature_importances_
        self.feature_names = self.X.columns
        self.feature_importance = pd.Series(self.importance, index=self.feature_names).sort_values(ascending=False)

        self.text+="------ Importances ------\n"
        self.text+=self.feature_importance.to_string()+"\n"

    def test(self):
        ## Testing

        self.text+="------------------------------------------------------------\n"

        predict = self.model_cb.predict(self.x_test)

        accuracy = accuracy_score(self.y_test, predict)
        self.text+="Accuracy : "+str(accuracy*100)+"%\n\n"

        cm = pd.DataFrame(
            confusion_matrix(self.y_test, predict),
            index = ["edible_data", "poisonous_data"],
            columns = ["edible_predict", "poisonous_predict"]
        )

        self.text+=cm.to_string()+"\n"

        self.text+="------------------------------------------------------------\n"

    def prod(self):
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

        self.text += "------ Données test (champignon) ------\n"

        for col, val in new_data.iloc[0].items():
            self.text += f"{col:<30} : {val}\n"

        self.text += "\n"

        # Prédiction
        pred = model_cb.predict(new_data)
        proba = model_cb.predict_proba(new_data)

        self.text+="Predicted class :"+str(pred[0])+"\n"
        self.text+="Probabilities  :"+str(proba[0])+"\n"

    def get_text(self):
        return self.text
