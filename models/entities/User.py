from werkzeug.security import check_password_hash

class User():
    
    def __init__(self, nombre_AS, documento, password, usuario, rol, estado):
        self.nombre_AS = nombre_AS
        self.documento = documento
        self.password = password
        self.usuario = usuario
        self.rol = rol
        self.estado = estado
    
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
#print(generate_password_hash("12345678"))
