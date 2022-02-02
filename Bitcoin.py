from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)
d=pd.read_csv(r'bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv')
model = pickle.load(open("bitcoin (1).pkl", "rb"))

@app.route("/")

def home():
    return render_template("Bitcoin.html")

@app.route("/predict", methods=["GET", "POST"])

def predict():
    if request.method == "POST":

        # Timestamp
        Timestamp = request.form["Timestamp"]
        day = int(pd.to_datetime(Timestamp, format="%Y-%m-%dT%H:%M").day)
        month = int(pd.to_datetime(Timestamp, format="%Y-%m-%dT%H:%M").month)
        year = int(pd.to_datetime(Timestamp, format="%Y-%m-%dT%H:%M").year)

        # Columns Reading
        Open = float(request.form["Open"])
        High = float(request.form["High"])
        Low = float(request.form["Low"])
        Close = float(request.form["Close"])
        Volume_BTC = float(request.form["Volume_BTC"])
        Volume_Currency = float(request.form["Volume_Currency"])

        prediction = model.predict([[Open,High,Low,Close,Volume_BTC,Volume_Currency,day,month,year]])

        output = round(prediction[0], 2)

        return render_template('Bitcoin.html', prediction_text="Bitcoin price is. {}".format(output))

    return render_template("Bitcoin.html")

if __name__ == "__main__":
    app.run(debug=True)