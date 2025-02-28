from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL


app=Flask(__name__)



# ---------------------------------------------------------------------------- #
#                                  Peticiones                                  #
# ---------------------------------------------------------------------------- #
@app.before_request
def before_request():
    print("Antes de la petición...")

   
@app.after_request
def after_request(response):
    print("Después de la petición")
    return response  



# ---------------------------------------------------------------------------- #
#                                Conexion MySQL                                #
# ---------------------------------------------------------------------------- #
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Kliiker'

conexion = MySQL(app)


@app.route('/consulta')
def listar_datos():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT prueba FROM prueba"
        cursor.execute(sql)
        listas=cursor.fetchall()
        #print(listas)
        data['listas'] = listas
        data['mensaje']='Exito'
    except Exception as ex:
        data['mensaje']='Error...'
    return jsonify(data)





@app.route('/')
def home():
   return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True, port=5000)