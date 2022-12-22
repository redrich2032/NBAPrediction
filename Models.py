import pandas as pd
import numpy as np

class Models:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        dataset = pd.read_csv(self.csv_file)
        self.X = dataset.iloc[:, :-1].values
        self.y = dataset.iloc[:, -1].values
        self.classifier = None
        self.y_pred = []
        self.X_train = [[]]
        self.X_test = [[]]
        self.y_train = []
        self.y_test = []
        self.accuracy_score = 0
        self.confusion_matrix = [[]]

    def preprocess_data(self):
        #encode categorical data (independent)
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse_output=False), [0, 1, 2, 3, 6 ,7])], remainder='passthrough')
        self.X = np.array(ct.fit_transform(self.X))

        #encode categorical data (dependent)
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        self.y = le.fit_transform(self.y)

        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X,self.y, test_size=0.2, random_state=0)

    def random_forest(self):
        #feature scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        self.X_train = sc.fit_transform(self.X_train)
        self.X_test = sc.transform(self.X_test)

        from sklearn.ensemble import RandomForestClassifier
        self.classifier=RandomForestClassifier(n_estimators=100, criterion = 'entropy', random_state= 0)
        self.classifier.fit(self.X_train,self.y_train)

        self.calculate_results()

    def naive_bayes(self):
        self.preprocess_data()
        from sklearn.naive_bayes import GaussianNB
        self.classifier = GaussianNB()
        self.classifier.fit(self.X_train, self.y_train)

        self.calculate_results()


    def calculate_results(self):
        # Predict Test Results
        self.y_pred = self.classifier.predict(self.X_test)

        from sklearn.metrics import confusion_matrix, accuracy_score
        self.confusion_matrix = confusion_matrix(self.y_test, self.y_pred)
        self.accuracy_score = accuracy_score(self.y_test, self.y_pred)

    def get_accuracy(self):
        return round(self.accuracy_score, 4)

    def get_confusion_matrix(self):
        return self.confusion_matrix