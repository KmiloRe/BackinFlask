from random import randrange
import flask
from ast import Match
# import sqlite3
import mysql.connector
from flask import Flask, request, jsonify, redirect, url_for, session,render_template
from mysql.connector import Error
from flask_cors import CORS,  cross_origin
# para login y registro
#Tokens con jwt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
#from flask.ext.cors import CORS, cross_origin
#Postgres tiene .Model, mysql NO, para esto importamos:
from flask_sqlalchemy import SQLAlchemy

#auth0 
#Jose Miguel
# para auth0 code de jose:
from authlib.integrations.flask_client import OAuth 
#estos 2 de abajo son para el manejo seguro de auth0, peroooo
#la seguridad es para miedosos
from dotenv import load_dotenv
import os


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#Para leer excel
import pandas as pd

#import pyodbc

#Jose Miguel

##Tengo muchos más imports de los necesarios


app = flask.Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Esta vivok!'
oauth = OAuth(app)
cors = CORS(app)
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app) # instancia de JWT

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
#Otros comandos no incluidos, se enncuentran en el readme en git                                                                                                       


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

# Daniel Dominguez
# codigo no usable
# db = SQLAlchemy(mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="my-secret-pw",
#   database="test"
# ))

#Daniel Dominguez

#Prueba simple de conexion
@app.route('/db_status')
def db_status():
    if mydb.is_connected():
        print("Conexion")
        return "Database connection successful!"
    else:
        print("Falla al conect")
        return "Database connection failed!"

#Jose Miguel

#Credenciales de auth0
#SEGURIDAD EN LOS DATOS?, No no la conozco
client_id = 'py3MmzYYQsrkOOSB4xaf7WZWvffXrrvl'
client_secret = 'jsZv4zL7kIfL5A0mb1rQE8HwPng5ennxm2NDxrhNrqeumDdAyswawvUGNNXehurF'
##<script src="https://cdn.auth0.com/js/auth0/9.12.1/auth0.min.js"></script>
##Este script debe ir en toda pagina html que use auth0

#blog.html tiene los componentes js necesarios para auth0
##Auth0, aun no funcional
@app.route('/loginauth0', methods=['GET'])
def loginauth0():
    #if consulta a la base de datos que usuario,clave = usuario, usuario.clave:
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

@app.route('/callback')
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    session['jwt_payload'] = userinfo
    print(session)
    return redirect('http://localhost/vidaNocturna')
#En este link iria la vista de usuario logeado

#Esta seria la pagina de usuario
@app.route('/dashboard')
def dashboard():
    if 'jwt_payload' not in session:
        return redirect(url_for('login'))
    return f"Welcome {session['jwt_payload']['name']}!"

#Jose Miguel

#Log in
@app.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    try:
        #uname=camilorestrerodriguez%40gmail.com&psw=gfgfgfgfgf&remember=on
        #request_data = json.loads(request.json)
        #email = request_data['email']
        username = request.json['uname']
        #username = 'camilo@camilosky.com.teodiohtmlvanila'
        clave = request.json['psw']
        print(username)
        print(clave)
        #clave = '123q'
        cursor = mydb.cursor()
        cursor.execute("SELECT clave from Users Where email='"+username+"'")
        ##reemplazar Users.id con el id sacado de un select
        results = cursor.fetchall()
        data = []
        for i in results:
                        data.append(i)
        #print()
        
        #Obtener el id para el token
        cursor2 = mydb.cursor()
        cursor2.execute("SELECT id from Users Where email='"+username+"'")
        results = cursor2.fetchall()
        data2 = []
        for i in results:
                        data2.append(i)
        #print()
        idd = str(data2[0][0])
        if(clave == str(data[0][0])):
             print('clave valida')
             #debe redirigir a una pagina (que aun no esta lista) de usuario logeado´
            # Crea un token de acceso para el usuario autenticado
             access_token = create_access_token(identity=idd)
             return jsonify({'access_token': access_token}), 200

             #return redirect("http://localhost:8080/contact.html", code=302)
        else:
             print('clave invalida')
             return redirect("http://localhost:8080/contact.html", code=302)#return a registro y en registro en else: return a index
    #Todo lo que retorna en web tiene que ser String 
    # return redirect() aun no funcional, mejor retornar un bool segun sugerencia del profe
    except Error as e:
        print("Error while connecting to MySQL", e)

randomglobarl = 0
@app.route('/readinfo', methods=['GET'])
@cross_origin(origin='*')
def read():
    try:
        cursor = mydb.cursor()
        randomid = randrange(1, 6)
        pppp = str(randomid) 
        randomglobarl = randomid
        cursor.execute("SELECT nombre from muchoslugares Where id='"+pppp+"'")
        results = cursor.fetchall()
        data = []
        for i in results:
                        data.append(i)
                        #print(data)

        #print(cursor.execute("SELECT id from Users Where id='1116241998'"))
        # response = {
        #     'message': 'Registro exitoso',
        #     'data': {
        #         'username': username,
        #         'email': email,
        #         'cellphone': cellphone
        #     }
        # }
        return str(data[0][0])
    #Todo lo que retorna en web tiene que ser String 
    except Error as e:
        print("Error while connecting to MySQL", e)

@app.route('/readimage', methods=['GET'])
@cross_origin(origin='*')
def readerimagen():
    try:
        cursor = mydb.cursor()
        randomid = randrange(1, 101)
        pppp = str(randomid) 
        cursor.execute("SELECT nombre from lugaresplataformas Where id='"+pppp+"'")
        results = cursor.fetchall()
        data = []
        for i in results:
                        data.append(i)
                        #print(data)
        cursor2 = mydb.cursor()
        cursor2.execute("SELECT imagen from lugaresplataformas Where id='"+pppp+"'")
        results2 = cursor.fetchall()
        data2 = []
        for i in results2:
                        data2.append(i)

        #print(cursor.execute("SELECT id from Users Where id='1116241998'"))
        # response = {
        #     'message': 'Registro exitoso',
        #     'data': {
        #         'username': username,
        #         'email': email,
        #         'cellphone': cellphone
        #     }
        # }
        #return str(data[0][0])

        cursor3 = mydb.cursor()
        cursor3.execute("SELECT descripcion from lugaresplataformas Where id='"+pppp+"'")
        results3 = cursor.fetchall()
        data3 = []
        for i in results3:
                        data3.append(i)
        
        cursor4 = mydb.cursor()
        cursor4.execute("SELECT instagram from lugaresplataformas Where id='"+pppp+"'")
        results4 = cursor.fetchall()
        data4 = []
        for i in results4:
                        data4.append(i)


        print('')
        second_string = str(data2[0][0]).replace('"','')
        print(second_string)
        return jsonify(
            nombre=str(data[0][0]),
            #instagram='https://www.instagram.com/accounts/login/',
            instagram=str(data4[0][0]),
            imagen= str(data2[0][0]), #second_string
            descripcion= str(data3[0][0])
        )
    #Todo lo que retorna en web tiene que ser String 
    except Error as e:
        print("Error while connecting to MySQL", e)
##Recomendaciones random
@app.route('/recomend', methods=['GET'])
@cross_origin(origin='*')
def recomend2():
    try:
        cursor = mydb.cursor()
        randomid = 2 #randrange(1, 6, 2) 
        cursor.execute("SELECT username from Users Where id=100000")
        results = cursor.fetchall()
        print(results)
        data = []
        for i in results:
                        data.append(i)
                        #print(data)

        #print(cursor.execute("SELECT id from Users Where id='1116241998'"))
        # response = {
        #     'message': 'Registro exitoso',
        #     'data': {
        #         'username': username,
        #         'email': email,
        #         'cellphone': cellphone
        #     }
        # }
        return str(data[0][0])
    #Todo lo que retorna en web tiene que ser String 
    except Error as e:
        print("Error while connecting to MySQL", e)
        return 'Error'+e



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
    return "Hello, from flask Back!"

# @app.route('/facts')
# def plano():
#     return "firebase db > flask + mysql"

###*************Metodos para cambio de contraseña

@app.route('/readoldpass', methods=['GET'])
@cross_origin(origin='*')
def readoldpass():
    # json or urlencode
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT username from Users Where id='1116241998'")
        results = cursor.fetchall()
        data = []
        for i in results:
                        data.append(i)
                        #print(data)

        #print(cursor.execute("SELECT id from Users Where id='1116241998'"))
        # response = {
        #     'message': 'Registro exitoso',
        #     'data': {
        #         'username': username,
        #         'email': email,
        #         'cellphone': cellphone
        #     }
        # }
        return str(data[0][0])
    #Todo lo que retorna en web tiene que ser String 
    except Error as e:
        print("Error while connecting to MySQL", e)


#Agregar un user

@app.route('/newuser', methods=['POST'])
@cross_origin(origin='*')
def data():

    #faltan verificaciones de calidad de datos
        #que no vengan vacios
        #que el correo si sea un correo
        #que la contraseña sea segura
    newusername = request.json['useruser']
    email = request.json['uname']
    clave = request.json['psw']
    # valores = flask.request.values
    # id = flask.request.values.get("id")
    # temp = flask.request.values.get("temperatura")
    # hum = flask.request.values.get("humedad")
    # luz = flask.request.values.get("luz")
    # maceta = flask.request.values.get("maceta")
    
    #valores = flask.request.values
    # se reemplaza esto por variables que vengan desde el front y listo
    # ya se pueden agregar usuarios
    #id = 1000002
    #temp = "Camilo"
    #hum = "camilo@camilosky.com.teodiohtmlvanila"
    luz = 3127403888
    #maceta = "Contraseñadsa"
    
    try:
        connection = mydb
        #mysql.connector.connect(
         # host='database-1.cg820r7giksa.us-east-1.rds.amazonaws.com', 
         # database='plantCare', user='admin', password='12345678')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            #print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            #recomendacion = recomendaciones(temp, hum, luz)
        #falta verificación de que el correo ingresado no exista ya

            cursor2 = connection.cursor()
            cursor2.execute("select max(id) from Users")
            results2 = cursor2.fetchall()
            data2 = []
            for i in results2:
                        data2.append(i)
        #print()
            idd3 = (data2[0][0]+1)
            print(idd3)
            #idd3 es el id max de la tabla +1, para mantener integridad
            #print(data2[0][0].type)
            #print(type(recomendacion))
            add_produto = """INSERT INTO Users(id,
                        username,email,cellphone,clave)
                        VALUES (%s, %s, %s,%s,%s)"""
            cursor.execute(
                add_produto, (idd3,newusername, email, luz, clave))
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.commit()
           # connection.close()
            #print("MySQL connection is closed")
    return 'registrado'
#enviar un bool y en front bool = true render x.html
#false, que se quede =
    #return newusername

#Metodo aun no usable, a corregir segun sugerencia del profe respecto a 
#render_template
@app.route("/historialrecomendaciones")
def main():
    recomend = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.TblCars")
    for row in cursor.fetchall():
        recomend.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("carslist.html", recomend = recomend)
    #return render_template("carslist.html", recomend = recomend)


#Metodos de prueba:


# @app.route('/registro', methods=['POST'])
# def register():
#     # valores = flask.request.values
#     # id = flask.request.values.get("id")
#     # temp = flask.request.values.get("temperatura")
#     # hum = flask.request.values.get("humedad")
#     # luz = flask.request.values.get("luz")
#     # maceta = flask.request.values.get("maceta")
    
#     #valores = flask.request.values
#     # se reemplaza esto por variables que vengan desde el front y listo
#     # ya se pueden agregar usuarios
#     id = 1000003
#     temp = "Chalarquin"
#     hum = "chalarca@camilosky.com.teodiohtmlvanila"
#     luz = 3127403888
#     maceta = "Contraseñadsa"
    
#     try:
#         connection = mydb
#         #mysql.connector.connect(
#          # host='database-1.cg820r7giksa.us-east-1.rds.amazonaws.com', 
#          # database='plantCare', user='admin', password='12345678')
#         if connection.is_connected():
#             db_Info = connection.get_server_info()
#             #print("Connected to MySQL Server version ", db_Info)
#             cursor = connection.cursor()
#             #recomendacion = recomendaciones(temp, hum, luz)

#             #print(type(recomendacion))
#             add_produto = """INSERT INTO Users(id,
#                         username,email,cellphone,clave)
#                         VALUES (%s, %s, %s,%s,%s)"""
#             cursor.execute(
#                 add_produto, (id,temp, hum, luz, maceta))
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.commit()
#            # connection.close()
#             #print("MySQL connection is closed")
#     return temp




#Codigo No usable

# Daniel Dominguez
#modelo (solo sirve si db is postgres sql)
# class Users(mydb.schema): # modelo de la tabla User
#     id = mydb.Column(mydb.Integer, primary_key=True)
#     username = mydb.Column(mydb.String(50), unique=True)
#     password = mydb.Column(mydb.String(50))
#     email = mydb.Column(mydb.String(50), unique=True)
#     cellphone = mydb.Column(mydb.Integer)
#     def __init__(self, username, password, email, cellphone):
#         self.username = username
#         self.password = password
#         self.email = email
#         self.cellphone = cellphone

#     def __repr__(self):
#         return f'<User {self.username}>'

# class Users(mydb):
#     __tablename__ = 'Users'
    
#     id = Column(Integer, primary_key=True)
#     username = Column(String(50), unique=True)
#     password = Column(String(50))
#     email = Column(String(50), unique=True)
#     cellphone = Column(Integer)
    
#     def __init__(self, username, password, email, cellphone):
#         self.username = username
#         self.password = password
#         self.email = email
#         self.cellphone = cellphone

#     def __repr__(self):
#         return f'<User {self.username}>'

# este codigo comentado de abajo funciona para Postgresql
# no se si funcione para Mysql

#with app.app_context():
#     mydb.create_all() # crea las tablas si no existen

#Mysql MOdel not working
# @app.route('/login', methods=['POST'])
# @cross_origin(origin='*')
# def login():
#     try:
#         username = request.json['username']
#         clave = request.json['clave']
#         #user = User.query.filter_by(username=username).first()
#         cursor = mydb.cursor()
#         cursor.execute("SELECT clave from Users WHERE username="+username)
#         results = cursor.fetchall()
#         if results == clave:
#             # Crea un token de acceso para el usuario autenticado
#             access_token = create_access_token(identity=Users.id)
#             return jsonify({'access_token': access_token}), 200
#         else:
#             return jsonify({'message': 'Credenciales inválidas'}), 401
#     except Error as e:
#         print("Error while connecting to MySQL", e)

# Query simple que trae un id
#Ejemplo de read con un query X a la BD

#Daniel Dominguez