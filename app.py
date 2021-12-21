from flask import Flask,url_for,render_template,redirect,request
import pickle

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('carprediction.html')



### result page
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        year = int(request.form['Year'])
        price = float(request.form['What is the Showroom Price?(In lakhs)'])
        kms = float(request.form['How Many Kilometers Drived?'])
        owners = int(request.form['How much owners previously had the car?'])
        fuel = request.form['What Is the Fuel type?']
        seller = request.form['Are you A Dealer or Individual?']
        transmission_type = request.form['Transmission type']

        if fuel == 'Petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0

        elif fuel == 'Diesel':
            fuel_type_petrol = 1
            fuel_type_diesel = 0

        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 0

        if seller == 'Dealer':
            seller_type_individual = 0

        else:
            seller_type_individual = 1

        if transmission_type == 'Manual car':
            transmission_manual = 1

        else:
            transmission_manual = 0

        year = 2020 - year

        prediction = model.predict([[price, kms, owners, year, fuel_type_diesel, fuel_type_petrol,
                                     seller_type_individual, transmission_manual]])

        output = round(prediction[0], 2)

        if output < 0:
            return render_template('result.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('result.html', prediction_text=f"You Can Sell The Car at {output} lakhs")
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)