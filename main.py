
from Models import Models
from WebScraper import WebScraper

model = Models('NBA.csv')
model.naive_bayes()
accuracy =model.get_accuracy()
accuracy = accuracy * 100
print("Bayes Accuracy: " + str(accuracy) + "%")

model.random_forest()
accuracy =model.get_accuracy()
accuracy = accuracy * 100
print("Random Forest Accuracy: " + str(accuracy) + "%")

# ws = WebScraper()
# ws.getPreviousMatchInfo("2022-10-18")
# ws.generate_csv()
