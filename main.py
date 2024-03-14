from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/vehicleregistration', methods=['GET','POST'])
def vehicleregistration():
    return render_template('vehicle_registration.html')

@app.route('/order', methods=['GET','POST'])
def placeorder():
    return render_template('order.html')



if __name__ == '__main__':
    app.run(debug=True)