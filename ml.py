from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def plot_data(dataFrame):
  dataFrame.plot(x = 'dates', y = 'rates', kind = 'line')
  plt.show()
  return

def preprocess(dataFrame):
    X, y = dataFrame.get(["dates"]), dataFrame.get(["rates"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

    poly = PolynomialFeatures(degree = 4)
    features_train = poly.fit_transform(X_train)
    features_test = poly.fit_transform(X_test)
    return (features_train, features_test, y_train, y_test, poly)

def training(X_train, X_test, y_train, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    print(model.score(X_train, y_train))
    print(model.score(X_test, y_test))
    return model

def get_X(poly, day):
    return poly.fit_transform([[32 + day]])

def predict_value(model, day):
    return model.predict(32 + day)


