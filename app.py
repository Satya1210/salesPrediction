from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__, template_folder="templates")

# Load the model
model2 = pickle.load(open('model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            Fat = float(request.form['Item_Fat_Content'])
            Item_type = float(request.form['Item_Type'])
            Location = float(request.form['Outlet_Location_Type'])
            Outlet_type = float(request.form['Outlet_Type'])
            Age = float(request.form['Age_Outlet'])
            Price = float(request.form['Item_MRP'])
            Visibility = float(request.form['Item_Visibility'])
            Brand = float(request.form['Brand'])

            prediction = model2.predict([[
                Fat, Visibility, Item_type, Price, Location, Outlet_type, Age,
                Brand
            ]])
            output = prediction[0]
            output = "{:.2f}".format(output)

            if float(output) < 10:  # Or some sensible threshold
                return render_template(
                    'index.html',
                    prediction_text=
                    "₹0.00 - Sales likely too low or data insufficient.")
            else:
                return render_template('index.html', prediction_text=output)

        except Exception as e:
            return render_template('index.html',
                                   prediction_text=f"Error: {str(e)}")
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
