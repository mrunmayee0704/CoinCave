import ml as model
from datetime import datetime, timedelta
from pandas import read_json, DataFrame
from requests import request

def menu() -> int:
  print("What do you want to do?")
  print("1.Convert\n2.View Historial rate\n3.See live rate(s)\n4.See Prediction for conversion rates")
  action = int(input("Enter corrsponding number: "))
  return action

def convert(url: str, header):
  to = str(input("enter:"))
  from_ = str(input("enter:"))
  amount = str(input("enter:"))
  url += "convert?to={to1}&from={from1}&amount={amount1}".format(to1 = to, from1 = from_, amount1 = amount)

  payload = {}
  response = request("GET", url, headers = header, data = payload)
  return response.text

def historical(url: str, header):
  date = str(input("enter date(YYYY-MM-DD):"))
  source = str(input("enter source currency code: "))
  currencies = str(input("enter currency code(s): "))
  url += "historical?date={date1}&source={source1}&currencies={currencies1}".format(date1 = date, source1 = source, currencies1 = currencies)
  
  payload = {}
  response = request("GET", url, headers = header, data = payload)
  return response.text

def live(url: str, header):
  source = input("enter source currency code: ")
  currencies = input("enter currency code(s): ")
  url += "live?source={source1}&currencies={currencies1}".format(source1 = source, currencies1 = currencies)

  payload = {}
  response = request("GET", url, headers = header, data = payload)
  return response.text

def get_date(now):
  mon = now[5:7]
  if mon == '01':
    month = '12'
    year = int(now[0:4]) - 1
  else:
    month = int(mon) - 1
    month = str(month).zfill(2)
    year = int(now[:4])
  date = f'{year}-{month}-{now[8:]}'
  return date

def timeframe(url: str, header):
  end_date = datetime.today().strftime('%Y-%m-%d')
  start_date = get_date(end_date)
  source = input("enter source currency code: ")
  currencies = input("enter currency code(s): ")
  day = int(input("Enter the number of days in future you want to predict for: "))
  url += "timeframe?start_date={start_date1}&end_date={end_date1}&source={source1}&currencies={currencies1}".format(start_date1 = start_date, end_date1 = end_date, source1 = source, currencies1 = currencies)

  payload = {}
  response = request("GET", url, headers = header, data = payload)
  return (response.text, day, source + currencies)

def get_rates(file: str, code: str):
  dataFrame = read_json(file)
  dataFrame = dataFrame.iloc[:, [-1]]
  rate = list(map(lambda x: x[0]['USDINR'], dataFrame.values))
  dataFrame.pop('quotes')
  dataFrame.insert(0, "rates", rate)
  dataFrame.insert(1, "dates", [_ for _ in range(len(dataFrame))])
  return dataFrame

def predict(file: str, day: int, code: str):
  dataFrame = get_rates(file, code)
  #model.plot_data(dataFrame)
  X_train, X_test, y_train, y_test, poly = model.preprocess(dataFrame)
  ml_model = model.training(X_train, X_test, y_train, y_test)

  X_features = model.get_X(poly, day)
  value = model.predict_value(ml_model, X_features)
  return value

