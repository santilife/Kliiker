from flask import Flask, render_template
from flask_mysqldb import MySQL


app=Flask(__name__)


# ---------------------------------------------------------------------------- #
#                                Conexion MySQL                                #
# ---------------------------------------------------------------------------- #
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Kliiker'

conexion = MySQL(app)





@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)