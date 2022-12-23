import pandas as pd
import numpy as np

class Models:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        dataset = pd.read_csv(self.csv_file)
        self.X = dataset.iloc[:, :-1].values
        self.y = dataset.iloc[:, -1].values
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []
        self.accuracy_score = 0
        self.confusion_matrix = [[]]

    def preprocess_data(self):
        #encode categorical data (independent)
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse_output=False), [0, 1, 2, 3, 6 ,7])], remainder='passthrough')
        X = np.array(ct.fit_transform(self.X))

        #encode categorical data (dependent)
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = le.fit_transform(self.y)

        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X,y, test_size=0.2, random_state=0)


        # feature scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        self.X_train = sc.fit_transform(self.X_train)
        self.X_test = sc.transform(self.X_test)


    def logistic_regression(self):
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression()
        classifier.fit(self.X_train, self.y_train)

        self.calculate_results(classifier)

    def decision_tree(self):
        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion = 'entropy', random_state=0)
        classifier.fit(self.X_train, self.y_train)
        self.calculate_results(classifier)

    def random_forest(self):
        from sklearn.ensemble import RandomForestClassifier
        classifier=RandomForestClassifier(n_estimators=100, criterion = 'entropy', random_state= 0)
        classifier.fit(self.X_train, self.y_train)

        self.calculate_results(classifier)
    def naive_bayes(self):
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        classifier.fit(self.X_train, self.y_train)

        self.calculate_results(classifier)
    def svm(self):
        from sklearn.svm import SVC
        classifier = SVC(kernel= 'linear', random_state= 0)
        classifier.fit(self.X_train, self.y_train)

        self.calculate_results(classifier)
    def svm_kernel(self):
        from sklearn.svm import SVC
        classifier = SVC(kernel= 'rbf', random_state= 0)
        classifier.fit(self.X_train, self.y_train)

        self.calculate_results(classifier)
    def knn(self):
        from sklearn.neighbors import KNeighborsClassifier
        classifier = KNeighborsClassifier(n_neighbors= 30, metric = 'minkowski', p = 2)
        classifier.fit(self.X_train, self.y_train)

        self.calculate_results(classifier)


    def calculate_results(self, classifier):
        # Predict Test Results
        y_pred = classifier.predict(self.X_test)

        from sklearn.metrics import confusion_matrix, accuracy_score
        self.confusion_matrix = confusion_matrix(self.y_test, y_pred)
        self.accuracy_score = accuracy_score(self.y_test, y_pred)

    def get_accuracy(self):
        return round(self.accuracy_score * 100, 2)

    def get_confusion_matrix(self):
        return self.confusion_matrix