import psycopg2
from flask import Flask, request, render_template, jsonify, session
import requests


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

@app.route('/vehicle_registration')
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


def get_last_client_data_from_database():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Query to retrieve the last inserted client data
        cursor.execute("SELECT id, cpf, cnpj FROM client ORDER BY id DESC LIMIT 1")
        last_client_data = cursor.fetchone()

        cursor.close()
        conn.close()
        
        return last_client_data
    except psycopg2.Error as e:
        print("Error retrieving last client data:", e)
        return None  # Return None if an error occurs
    
def get_last_veiculo_data_from_database():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT placa FROM veiculo ORDER BY id DESC LIMIT 1")
        last_veiculo_data = cursor.fetchone()

        cursor.close()
        conn.close()

        return last_veiculo_data
    except psycopg2.Error as e:
        print("Error retrieving last veiculo data")
        return None # Return None if an error occurs


# Route to retrieve the last inserted client data
@app.route('/get_last_client_data', methods=['GET'])
def get_last_client_data():
    last_client_data = get_last_client_data_from_database()
    if last_client_data:
        client_id, cpf, cnpj = last_client_data
        return jsonify({'client_id': client_id, 'cpf': cpf, 'cnpj': cnpj}), 200
    else:
        return jsonify({'error': 'Failed to retrieve last client data'}), 404




# Route to retrieve the last placa from the veiculo table
@app.route('/get_last_veiculo_data', methods=['GET'])
def get_last_veiculo_data():
    last_placa = get_last_veiculo_data_from_database()
    if last_placa:
        return jsonify({'last_placa': last_placa}), 200
    else:
        return jsonify({'error': 'Failed to retrieve last placa'}), 404


# # Route to fetch tiposervicos from the database
# @app.route('/get_tiposervicos', methods=['GET'])
# def get_tiposervicos():
#     tiposervicos = fetch_tiposervicos_from_database()
#     if tiposervicos:
#         return jsonify({'tiposervicos': tiposervicos}), 200
#     else:
#         return jsonify({'error': 'Failed to retrieve tiposervicos'}), 404


@app.route('/view/<int:selected_client_id>', methods=['GET'])
def view_client(selected_client_id):
    if selected_client_id:
        conn = get_db()  
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM client WHERE id = %s"
            cursor.execute(query, (selected_client_id,))
            client_info = cursor.fetchone()

            if client_info:
                client_dict = {
                    'client_id': client_info[0],
                    'clientName': client_info[1],
                    'cpf': client_info[2],
                    'RazaoSocial': client_info[3],
                    'cnpj': client_info[4],
                    'Telephone': client_info[5],
                    'Cellphone': client_info[6],
                    'Email1': client_info[7],
                    'Email2': client_info[8],
                    'CEP': client_info[9],
                    'Logradouro': client_info[10],
                    'Numero': client_info[11],
                    'Complemento': client_info[12],
                    'brazilianStates': client_info[13],
                    'city': client_info[14]
                }
                return jsonify(client_dict)
            else:
                return jsonify({'error': 'Client not found'})

        except psycopg2.Error as e:
            print("Error fetching client information:", e)
            return jsonify({'error': 'Database error'})

        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'No client selected'})
    

@app.route('/searchdatabase', methods=['GET'])
def search():
    if request.method == 'GET':
        search_param = request.args.get('procura')
        print("Search parameter:", search_param) 
        if search_param:
            conn = get_db()
            cursor = conn.cursor()

            try:
                query = "SELECT id, clientname, cpf, cnpj, email1, cellphone FROM client WHERE clientname ILIKE %s OR email1 ILIKE %s OR cellphone ILIKE %s OR cpf ILIKE %s OR cnpj ILIKE %s;"
                cursor.execute(query, (f"%{search_param}%", f"%{search_param}%", f"%{search_param}%", f"%{search_param}%", f"%{search_param}%"))
                records = cursor.fetchall()

                if records:
                    search_results = [dict(zip([column.name for column in cursor.description], row)) for row in records]
                else:
                    search_results = []
            except psycopg2.Error as e:
                print("Error fetching records:", e)
                search_results = []
            finally:
                cursor.close()
                conn.close()

            print("Search results:", search_results) 
            return render_template('search.html', search_results=search_results)
        else:
            return render_template('search.html', search_results=[])


@app.route('/search_client', methods=['POST'])
def search_client():
    if request.method == 'POST':
        cpf_cnpj = request.form.get('cpfCnpj')
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, clientname, cpf, cnpj FROM client WHERE cpf = %s OR cnpj = %s', (cpf_cnpj, cpf_cnpj))
        client_data = cursor.fetchone()

        if client_data:
            client_id, clientname, cpf, cnpj = client_data
            client_info = {
                'client_id': client_id,
                'clientname': clientname,
                'cpfCnpj': cpf if cpf else cnpj,
                'veiculos': []
            }

            cursor.execute('SELECT id, placa FROM veiculo WHERE client_id = %s', (client_id,))
            veiculos = cursor.fetchall()

            for veiculo_id, placa in veiculos:
                veiculo_info = {'id': veiculo_id, 'placa': placa, 'servicos': []}
                cursor.execute('SELECT nome FROM tipo_de_servico WHERE id_veiculo = %s', (veiculo_id,))
                servicos = cursor.fetchall()
                for servico in servicos:
                    veiculo_info['servicos'].append(servico[0])
                
                # Append veiculo_info to client_info
                client_info['veiculos'].append(veiculo_info)

            cursor.close()
            conn.close()

            return jsonify(client_info)
        else:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Cliente não encontrado'}), 404



@app.route('/vehicle_registration', methods=['POST'])
def vehicle_registration():
    if request.method == 'POST':
        # Process the form data
        client_id = request.form.get('client_id')
        placa = request.form.get('placa')
        cpf = request.form.get('cpf')
        cnpj = request.form.get('cnpj')
        chassi = request.form.get('chassi')
        fabricante = request.form.get('fabricante')
        modelo = request.form.get('modelo')
        cor = request.form.get('cor')
        ano_modelo = request.form.get('ano_modelo')

        if placa and (cpf or cnpj) and chassi and fabricante and cor and ano_modelo:
            # Insert the data into the database
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO veiculo (placa, cpf, cnpj, chassi, fabricante, modelo, cor, ano_modelo, client_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                                (placa, cpf, cnpj, chassi, fabricante, modelo, cor, ano_modelo, client_id))
            conn.commit()
            cursor.close()
            return render_template('vehicle_registration.html', placa=placa)  # Redirect to a success page or another route
        else:
            flash('Try Again.', 'error')
            return render_template('vehicle_registration.html', placa=request.args.get('placa'))
    else:
        # If it's a GET request, render the vehicle registration page
        placa = request.args.get('placa')
        

        # Store client_id, cpf, and cnpj in session
        session['placa'] = placa
       

        return render_template('vehicle_registration.html', placa=placa)


@app.route('/show_ordem', methods=['GET'])
def show_ordem():
    # Get the last client ID
    last_client_id_response = requests.get('http://localhost:5021/get_last_client_data')
    if last_client_id_response.status_code == 200:
        last_client_id = last_client_id_response.json()['client_id']
    else:
        last_client_id = None

    # Get the last placa
    last_placa_response = requests.get('http://localhost:5021/get_last_veiculo_data')
    if last_placa_response.status_code == 200:
        last_placa = last_placa_response.json()['last_placa']
    else:
        last_placa = None
    
    tiposervicos = get_tiposervicos()


    # Render the template with the data
    return render_template('show_ordem.html', last_client_id=last_client_id, last_placa=last_placa, tiposervicos=tiposervicos)



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
    app.run(debug=True, port='5021')
