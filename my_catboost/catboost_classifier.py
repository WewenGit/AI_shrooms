import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class CatBoostAnalyzer():
    
    def __init__(self):
        self.data = pd.read_csv("./mushroom/agaricus_lepiota.csv")
        self.target = "poisonous"


        ## Data cleaning
        self.data = self.data.drop(columns=["veil-type"])


        ## Infos
        print(self.data[self.target].value_counts())
        print(self.data.info())
        #print(data.describe())
        print()


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

        print("------ Importances ------")
        print(self.feature_importance)

    def test(self):
        ## Testing

        print(f"------------------------------------------------------------")

        predict = self.model_cb.predict(self.x_test)

        accuracy = accuracy_score(self.y_test, predict)
        print(f"Accuracy : {accuracy*100} %\n")

        confusion_matrix = pd.DataFrame(
            confusion_matrix(self.y_test, predict),
            index = ["edible_data", "poisonous_data"],
            columns = ["edible_predict", "poisonous_predict"]
        )

        print(confusion_matrix)

        print(f"------------------------------------------------------------")

    def prod(self):
        ## Production : Export model
        self.model_cb.save_model("cb_model.cbm")
