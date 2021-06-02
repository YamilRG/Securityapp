from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/apiyamil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    Inf_Producto = db.Column(db.String(100))

    def __init__(self, nombre, Inf_Producto):
        self.nombre = nombre
        self.Inf_Producto = Inf_Producto


class Productchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'Inf_Producto')

product_schema = Productchema()
products_schema = Productchema(many=True)


#Ruta para insertar datos con post
@app.route('/producto', methods=['POST'])
def create_product():

    nombre = request.json['nombre']
    Inf_Producto = request.json['Inf_Producto']

    new_product = productos(nombre, Inf_Producto)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


#Ruta para tener todas las tareas
@app.route('/productos', methods=['GET'])
def get_tasks():

    #Lista de las cosas y se guarda en la variable result
    all_product = productos.query.all()
    result = products_schema.dump(all_product)

    return jsonify(result)



@app.route('/productos/<id>', methods=['PUT'])
def update_todo_by_id(id):
   data = request.get_json()
   get_todo = productos.query.get(id)
   if data.get('nombre'):
       get_todo.title = data['nombre']
   if data.get('Inf_Producto'):
       get_todo.todo_description = data['Inf_Producto']
   db.session.add(get_todo)
   db.session.commit()
   todo_schema = products_schema(only=['id', 'nombre', 'Inf_Producto'])
   todo = todo_schema.dump(get_todo)

   return products_schema(jsonify({"todo": todo}))


@app.route('/productos/<id>', methods=['DELETE'])
def delete_todo_by_id(id):
   get_product = productos.query.get(id)
   db.session.delete(get_product)
   db.session.commit()
   return products_schema("", 204)









if __name__ == "__main__":
    app.run(debug=True)