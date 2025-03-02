from flask_mysqldb import MySQL

# Models
# Entities


mysql = MySQL()


# db = MySQL(app)

# ---------------------------------------------------------------------------- #
#                                Conexion MySQL                                #
# ---------------------------------------------------------------------------- #

def db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'Kliiker'

    mysql.init_app(app)



