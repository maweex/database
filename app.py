from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:autonoma@database:5432/uautonoma'

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    numero = db.Column(db.Integer, nullable=True)



@app.route('/usuarios', methods= ['POST'])
def index():
    datos = request.get_json()
    print (datos)

    usuario = Usuario(**datos)

    db.session.add(usuario)
    db.session.commit()


    return usuarioDictionary(usuario), 201


@app.route('/usuarios', methods=['GET'])
def mostrarUsuarios():
    usuarios = Usuario.query.all()

    lista_usuarios = []
    for usuario in usuarios:
        lista_usuarios.append(usuarioDictionary(usuario))

    return jsonify(lista_usuarios), 200


@app.route('/usuarios/<id>', methods=['GET'])
def especificarUsuario(id):
    usuario = Usuario.query.get_or_404(id)

    return usuarioDictionary(usuario),200


@app.route('/usuarios/<id>', methods=['PUT'])
def actualizarUsuario(id):
    usuario = Usuario.query.get_or_404(id)
    datos = request.get_json()

    usuario.nombre = datos['nombre']
    usuario.email = datos['email']
    usuario.password = datos['password']
    usuario.numero = datos['numero']

    db.session.add(usuario)
    db.session.commit()
        
    return usuarioDictionary(usuario),200

@app.route('/usuarios/<id>', methods=['DELETE'])
def borrarUsuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()

    return '', 204

def usuarioDictionary(usuario):
    return {
        
          'id': usuario.id,
          'nombre': usuario.nombre,
          'email': usuario.email,
          'numero': usuario.numero
    }