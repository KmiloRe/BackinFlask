import flask
from ast import Match
# import sqlite3
import mysql.connector

from flask import Flask, request, jsonify
from mysql.connector import Error
from flask_cors import CORS,  cross_origin
# para login y registro
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
#from flask.ext.cors import CORS, cross_origin


#este flask requiere AXIOS para conectar correctamente con el front
# es un back muy sencillo pero tiene algunas funciones extras
# como la pseudo IA de recomendaciones (el if anidado)


#saque estos comandos de mi historial de comandos
#puede que no todos sean necesarios y que incluso
#puede faltar alguno
#npm i axios -S       
#python -m pip install flask_cors  
#python3 -m pip install Flask  
#python -m flask run    
# pip install -r requirements.txt                                                       
                                                                                                       
app = flask.Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Esta vivok!'

cors = CORS(app)

#Conexion a mysql
#la base de datos se encuentra corriendo en un docker
# el docker tiene las siguientes conexiones
#para el correcto funcionamiento se debe tener docker
# con una imagen de mysql segun el readme
# y el contenedor debe estar prendido
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="my-secret-pw",
  database="test"
)

#Prueba simple de conexion
@app.route('/db_status')
def db_status():
    if mydb.is_connected():
        print("Conexion")
        return "Database connection successful!"
    else:
        print("Falla al conect")
        return "Database connection failed!"

# modelo
class User(mydb.Model): # modelo de la tabla User
    id = mydb.Column(mydb.Integer, primary_key=True)
    username = mydb.Column(mydb.String(50), unique=True)
    password = mydb.Column(mydb.String(50))
    email = mydb.Column(mydb.String(50), unique=True)
    cellphone = mydb.Column(mydb.Integer)
    def __init__(self, username, password, email, cellphone):
        self.username = username
        self.password = password
        self.email = email
        self.cellphone = cellphone

    def __repr__(self):
        return f'<User {self.username}>'

# este codigo comentado de abajo funciona para Postgresql
# no se si funcione para Mysql

# with app.app_context():
#     mydb.create_all() # crea las tablas si no existen

#Log in
@app.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Crea un token de acceso para el usuario autenticado
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Error as e:
        print("Error while connecting to MySQL", e)

# Registrarme
@app.route('/register', methods=['POST'])
@cross_origin(origin='*')
def register():
    try:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        cellphone = request.json['cellphone']
        user = User(username, password, email, cellphone)
        mydb.session.add(user) # agrega el usuario a la base de datos
        mydb.session.commit() # guarda los cambios en la base de datos
        response = {
            'message': 'Registro exitoso',
            'data': {
                'username': username,
                'email': email,
                'cellphone': cellphone
            }
        }
        return jsonify(response), 200
    except Error as e:
        print("Error while connecting to MySQL", e)


#Este recomendaciones es de un trabajo de telematica, 
#podemos usar algo parecido en caso de 
#No estar listo el modelo de IA, para quemar las recomendaciones en codigo
def recomendaciones(temp, hum, luz):
    recomendacion = ""
    if float(temp) > 28:
        if float(hum) > 70 or float(hum) < 50:
            recomendacion = "Riega la planta, falta de humedad"
        else:
            recomendacion = "Tu planta está bien"
    elif float(temp) < 10:
        if float(hum) > 50:
            recomendacion = "No riegues más tu planta, puede sufrir quemaduras"
        elif float(hum) > 50:
            recomendacion = "Riegala planta, pones en riesgo sus tejidos celulares"
        else:
            recomendacion = "Tu planta está bien"
    else:
        if float(hum) < 20:
            recomendacion = "Riega tu planta"
        else:
            recomendacion = "Tu planta está bien"
    return recomendacion

#Si la base estubiera en aws, el config de conexion:
# config = {
#   ‘user’: ‘root’,
#   ‘password’: ‘my-secret-pw’,
#   ‘host’: ‘db’,
#   ‘port’: ‘3306’,
#   ‘database’: ‘knights’
# }
# connection = mysql.connector.connect(**config)


# @app.route('/data', methods=['POST'])
# def data():
#     valores = flask.request.values
#     id = flask.request.values.get("id")
#     temp = flask.request.values.get("temperatura")
#     hum = flask.request.values.get("humedad")
#     luz = flask.request.values.get("luz")
#     maceta = flask.request.values.get("maceta")

#     try:
#         connection = mydb
#         #mysql.connector.connect(
#          # host='database-1.cg820r7giksa.us-east-1.rds.amazonaws.com', 
#          # database='plantCare', user='admin', password='12345678')
#         if connection.is_connected():
#             db_Info = connection.get_server_info()
#             print("Connected to MySQL Server version ", db_Info)
#             cursor = connection.cursor()
#             recomendacion = recomendaciones(temp, hum, luz)

#             print(type(recomendacion))
#             add_produto = """INSERT INTO plantHistory(temp,
#                         hum,luz, maceta,recomendacion)
#                         VALUES (%s, %s, %s,%s,%s)"""
#             cursor.execute(
#                 add_produto, (temp, hum, luz, maceta, recomendacion))
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.commit()
#             #connection.close()
#             #print("MySQL connection is closed")
#     return recomendacion


# @app.route('/user', methods=['POST'])
# def user():
#     usuario = flask.request.values.get("usuario")
#     data = []
#     try:
#         connection = mysql.connector.connect(
#             #460ab13cf22a #172.17.0.2
#             host='localhost', database='test', user='root', password='my-secret-pw')
#         if connection.is_connected():
#             db_Info = connection.get_server_info()
#             print("Connected to MySQL Server version ", db_Info)
#             cursor = connection.cursor()
#             add_produto = """SELECT * from plantHistory WHERE maceta=(%s)"""
#             cursor.execute("SELECT * from plantHistory WHERE maceta="+usuario)
#             results = cursor.fetchall()
#     # print(results)
#             for i in results:
#                 data.append(i)
#             print(data)

#     except Error as e:
#         print("Error while connecting to MySQL", e)
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.commit()
#             connection.close()
#             print("MySQL connection is closed")
#     return {"data": data}


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
@app.route('/contact')
def plano():
    return "Gas HTml"

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/facts')
def plano():
    return "firebase db > flask + mysql"