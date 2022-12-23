
from Models import Models
#from WebScraper import WebScraper

model = Models('NBA.csv')
model.preprocess_data()

model.logistic_regression()
accuracy= model.get_accuracy()
print("Logistic Regression Accuracy: " + str(accuracy) + "%")

model.decision_tree()
accuracy = model.get_accuracy()
print("Decision Tree Accuracy: " + str(accuracy) + "%")

model.random_forest()
accuracy =model.get_accuracy()
print("Random Forest Accuracy: " + str(accuracy) + "%")

model.naive_bayes()
accuracy =model.get_accuracy()
print("Bayes Accuracy: " + str(accuracy) + "%")

model.svm()
accuracy = model.get_accuracy()
print("SVM Accuracy: " + str(accuracy) + "%")

model.svm_kernel()
accuracy = model.get_accuracy()
print("SVM Kernel Accuracy: " + str(accuracy) + "%")

model.knn()
accuracy = model.get_accuracy()
print("KNN Accuracy: " + str(accuracy) + "%")


# ws = WebScraper()
# ws.getPreviousMatchInfo("2022-10-18")
# ws.generate_csv()
