from dbmaster import db_reader
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
import pickle

tuple_data = db_reader("forecast_puredataset", 9, 1)
data = pd.DataFrame(tuple_data[0], columns=['id', 'year', 'month', 'day', 'baar', 'time', 'eldata', 'tmdata', 'hddata'])
print(type(data))
print(data.head())
# print(data.tail())
le = preprocessing.LabelEncoder()
year = le.fit_transform(list(data["year"]))
month = le.fit_transform(list(data["month"]))
day = le.fit_transform(list(data["day"]))
baar = le.fit_transform(list(data["baar"]))
time = le.fit_transform(list(data["time"]))
tmdata = le.fit_transform(list(data["tmdata"]))
eldata = le.fit_transform(list(data["eldata"]))
hddata = le.fit_transform(list(data["hddata"]))
edexact = list(data["eldata"])
# print(edexact)
yr = data["year"]
mn = data["month"]
dy = data["day"]
br = data["baar"]
tm = data["time"]
print(type(yr))

predict = "eldata"

x = list(zip(month, day, baar, time, eldata))
y = list(eldata)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors=100)

model.fit(x_train, y_train)
acc = model.score(x_test, y_test)

predicted = model.predict(x_test)
perfect = 0
match = 0
unmatch = 0
total = 0
for x in range(len(predicted)):
    print("Predicted: ", edexact[predicted[x]], "Data: ", data["month"][x_test[x][0]], data["day"][x_test[x][1]],
          data["baar"][x_test[x][2]], data["time"][x_test[x][3]], " Actual: ", edexact[y_test[x]])
    n = model.kneighbors([x_test[x]], 200, True)
    if float(edexact[predicted[x]]) == float(edexact[y_test[x]]):
        perfect += 1;
        print("perfect")
    elif abs(float(edexact[predicted[x]]) - float(edexact[y_test[x]])) < 0.1:
        match += 1;
        print("matched", edexact[y_test[x]], edexact[predicted[x]])
    else:
        unmatch += 1;
        print("unmatched")
    total += 1
    # print("N: ",n)
print("Perfect: ", perfect, " Matched :", match, " Unmatched: ", unmatch, " Total: ", total)
print("Slight Accuracy: ", (match + perfect) * 100 / total)
print("Raw Accuracy: ", acc)

if ((match + perfect) * 100 / total) > 60:
    with open("puredataset.pickle", "wb") as f:
        pickle.dump(model, f)
        print("saved")
