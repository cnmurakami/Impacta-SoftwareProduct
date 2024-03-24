import psycopg2
from flask import Flask, request, render_template


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

def get_db():
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname="car_automotive",
        user="postgres",
        password="Private@17",
        host="localhost",
        port=5433
    )
    return conn

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/order', methods=['GET'])
def order_page():
    return render_template('order.html')

@app.route('/register_vehicle')
def register_vehicle_page():
    return render_template('vehicle_registration.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        if request.method == 'POST':
            clientName = request.form['clientName']
            CPF = request.form['CPF']
            RazaoSocial = request.form['RazaoSocial']
            CNPJ = request.form['CNPJ']
            Telephone = request.form['Telephone']
            Cellphone = request.form['Cellphone']
            Email1 = request.form['Email1']
            Email2 = request.form['Email2']
            CEP = request.form['CEP']
            Logradouro = request.form['Logradouro']
            Numero = request.form['Numero']
            Complemento = request.form['Complemento']
            brazilianStates = request.form['brazilianStates']
            city = request.form['city']
            if ((clientName and CPF) or (RazaoSocial and CNPJ)) and (Telephone or Cellphone) and (Email1 or Email2) and CEP:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO client (clientname, cpf, razaosocial, cnpj, telephone, cellphone, email1, email2, cep, logradouro, numero, complemento, brazilianstates, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (clientName, CPF, RazaoSocial, CNPJ, Telephone, Cellphone, Email1, Email2, CEP, Logradouro, Numero, Complemento, brazilianStates, city))
                conn.commit()
                cursor.close()
                return render_template('vehicle_registration.html')
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"An error occurred: {str(e)}")
        return render_template('register.html'), 500
    return render_template('register.html')



@app.route('/searchdatabase', methods=['GET'])
def search():
    if request.method == 'GET':
        search_param = request.args.get('procura')
        print("Search parameter:", search_param)  # Debug print
        if search_param:
            # Connect to the database
            conn = get_db()
            cursor = conn.cursor()

            try:
                # Use ILIKE for case-insensitive search
                query = "SELECT * FROM client WHERE clientname ILIKE %s OR email1 ILIKE %s OR cellphone ILIKE %s OR cpf ILIKE %s OR cnpj ILIKE %s;"
                cursor.execute(query, (f"%{search_param}%", f"%{search_param}%", f"%{search_param}%", f"%{search_param}%", f"%{search_param}%"))
                records = cursor.fetchall()

                if records:
                    # Convert records to list of dictionaries
                    search_results = [dict(zip([column.name for column in cursor.description], row)) for row in records]
                else:
                    search_results = []
            except psycopg2.Error as e:
                print("Error fetching records:", e)
                search_results = []
            finally:
                cursor.close()
                conn.close()

            print("Search results:", search_results)  # Debug print
            return render_template('search.html', search_results=search_results)
        else:
            # If no search parameter provided, render empty search page
            return render_template('search.html', search_results=[])


    

if __name__ == "__main__":
    app.run(debug=True, port='5014')
