
from flask import Flask, request, render_template, jsonify, session, flash
import pymysql


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages


def get_db():
    # Connect to your MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Unitario321',
        database='rscarautomotive',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
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
    return render_template('show_ordem.html')

@app.route('/vehicle_registration')
def register_vehicle_page():
    return render_template('vehicle_registration.html')

@app.route('/status', methods=['GET'])
def status_page():
    return render_template('status.html')

@app.route('/ordem', methods=['GET'])
def show_ordem_page():
    return render_template('ordem.html')



@app.route('/register', methods=['POST'])
def register():
    try:
        if request.method == 'POST':
            # Retrieve form data
            clientName = request.form['clientName']
            CPF = request.form['CPF']
            RazaoSocial = request.form['RazaoSocial']
            CNPJ = request.form['CNPJ']
            Cellphone = request.form['Cellphone']
            Email1 = request.form['Email1']
            CEP = request.form['CEP'][:8] 
            Logradouro = request.form['Logradouro']
            Numero = request.form['Numero']
            Complemento = request.form['Complemento']
            brazilianStates = request.form['brazilianStates']
            city = request.form['city']

            endereco = Logradouro + Complemento + Numero + city + brazilianStates + CEP

            app.logger.info(f"Form data received: {request.form}")

            # Check if required fields are present
            if ((clientName and CPF) or (RazaoSocial and CNPJ)) and Cellphone and Email1 and CEP:
                # Insert data into the database
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO cliente (nome, cpf, razao_social, cnpj, telefone, email, endereco) VALUES (%s, %s, %s, %s, %s, %s, %s)', (clientName, CPF, RazaoSocial, CNPJ, Cellphone, Email1, endereco))
                conn.commit()
                cursor.close()
                app.logger.info("Data inserted successfully")
                return render_template('vehicle_registration.html')
            else:
                app.logger.error("One or more required fields are missing")
                return render_template('register.html', error='One or more required fields are missing'), 400
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"An error occurred: {str(e)}")
        return render_template('register.html'), 500
    return render_template('register.html')


# @app.route('/register', methods=['POST'])
# def register():
#     try:
#         if request.method == 'POST':
#             # Retrieve form data
#             clientName = request.form['clientName']
#             CPF = request.form['CPF']
#             RazaoSocial = request.form['RazaoSocial']
#             CNPJ = request.form['CNPJ']
#             Cellphone = request.form['Cellphone']
#             Email1 = request.form['Email1']
#             CEP = request.form['CEP'][:8] 
#             Logradouro = request.form['Logradouro']
#             Numero = request.form['Numero']
#             Complemento = request.form['Complemento']
#             brazilianStates = request.form['brazilianStates']
#             city = request.form['city']

#             app.logger.info(f"Form data received: {request.form}")

#             # Check if required fields are present
#             if ((clientName and CPF) or (RazaoSocial and CNPJ)) and Cellphone and Email1 and CEP:
#                 # Insert data into the database
#                 conn = get_db()
#                 cursor = conn.cursor()
#                 cursor.execute('INSERT INTO client (clientname, cpf, razaosocial, cnpj, cellphone, email1, cep, logradouro, numero, complemento, brazilianstates, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (clientName, CPF, RazaoSocial, CNPJ, Cellphone, Email1, CEP, Logradouro, Numero, Complemento, brazilianStates, city))
#                 conn.commit()
#                 cursor.close()
#                 app.logger.info("Data inserted successfully")
#                 return render_template('vehicle_registration.html')
#             else:
#                 app.logger.error("One or more required fields are missing")
#                 return render_template('register.html', error='One or more required fields are missing'), 400
#     except Exception as e:
#         # Log the error for debugging purposes
#         app.logger.error(f"An error occurred: {str(e)}")
#         return render_template('register.html'), 500
#     return render_template('register.html')



@app.route('/get_last_client_data', methods=['GET'])
def get_last_client_data():
    last_client_data = get_last_client_data_from_database()
    if last_client_data:
        # id_cliente, cpf, cnpj = last_client_data
        return jsonify(last_client_data), 200
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


@app.route('/get_last_client_data_from_database', methods=['GET'])
def get_last_client_data_from_database():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Query to retrieve the last inserted client data
        cursor.execute("SELECT id_cliente, cpf, cnpj FROM cliente ORDER BY id_cliente DESC LIMIT 1")
        last_client_data = cursor.fetchone()

        cursor.close()
        conn.close()
        
        return last_client_data
    except pymysql.Error as e:
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
    
def get_tipo_servicos():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tipo_servico ORDER BY id")
        tiposervicos = cursor.fetchone()

        cursor.close()
        conn.close()

        return tiposervicos
    except psycopg2.Error as e:
        print("Error retrieving tipo_servico data")
        return None



@app.route('/view/<int:selected_client_id>', methods=['GET'])
def view_client(selected_client_id):
    if selected_client_id:
        conn = get_db()  
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM cliente WHERE id_cliente = %s"
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
def search_database():
    if request.method == 'GET':
        search_param = request.args.get('procura')
        print("Search parameter:", search_param) 
        if search_param:
            conn = get_db()
            cursor = conn.cursor()

            try:
                query = "SELECT id_cliente, nome, cpf, cnpj, email, telefone FROM cliente WHERE nome ILIKE %s OR email ILIKE %s OR telefone ILIKE %s OR cpf ILIKE %s OR cnpj ILIKE %s;"
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
        
        cursor.execute('SELECT cliente_id, nome, cpf, cnpj FROM cliente WHERE cpf = %s OR cnpj = %s', (cpf_cnpj, cpf_cnpj))
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
        id_cliente = request.form.get('id_cliente')
        placa = request.form.get('placa')
        cpf = request.form.get('cpf')
        cnpj = request.form.get('cnpj')
        chassi = request.form.get('chassi')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        cor = request.form.get('cor')
        ano_modelo = request.form.get('ano_modelo')
        ano_fabricacao = request.form.get('ano_fabricacao')

        if placa and chassi and marca and cor and ano_modelo:
            # Insert the data into the database
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO veiculo (placa, chassi, marca, modelo, cor, ano_modelo, id_cliente, ano_fabricacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                                                (placa, chassi, marca, modelo, cor, ano_modelo, id_cliente, ano_fabricacao))
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
    last_client_id_response = request.get('http://localhost:5021/get_last_client_data')
    if last_client_id_response.status_code == 200:
        last_client_id = last_client_id_response.json()['client_id']
    else:
        last_client_id = None

    # Get the last placa
    last_placa_response = request.get('http://localhost:5021/get_last_veiculo_data')
    if last_placa_response.status_code == 200:
        last_placa = last_placa_response.json()['last_placa']
    else:
        last_placa = None
    
    tiposervicos = get_tipo_servicos()


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
