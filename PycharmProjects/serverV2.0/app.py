from flask import Flask, request
from DataServiceFile import DBDataService, IDataService
# import pickle
# from model import *
#
# with open('./data/seq2seq.pk', 'rb') as f:
#     data = pickle.load(f)
# input_lang = data['input_lang']
# output_lang = data['output_lang']
# encoder = data['encoder']
# attn_decoder = data['attn_decoder']
# hidden_size = encoder.hidden_size
#
#
# print(get_answer("привет", input_lang, output_lang, encoder, attn_decoder))

# Init app
app = Flask(__name__)

# Initialize data service
ds = DBDataService()



@app.route('/help', methods=['GET'])
def help():
    return "-help\n-save_message\n-get_history\n-add_user\nsmth else\n"


@app.route('/get_history/<id>', methods=['GET'])
def get_history(id):
    return ds.get_history(id)


@app.route('/get_ans/<id>', methods=['POST'])
def get_ans(id):
    s = str(request.get_data())
    # print(s[2:-1])
    return "Yeah" + s
    # ds.save_message(s, "wow cool", id)
    # return ds.get_history(id)


@app.route('/del/<id>', methods=['GET'])
def del_history(id):
    ds.del_history(id)
    return ds.get_history(id)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = str(request.get_data())
    usrName = name[2:-1]
    newUserID = ds.add_user_withoutID(usrName)
    return str(newUserID)


@app.route('/find_user', methods=['POST'])
def find_user():
    name = str(request.get_data())
    usrName = name[2:-1]
    newUserID = ds.find_usr(usrName)
    return str(newUserID)





















'''


basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise db
db = SQLAlchemy(app)

# Initialise ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get all Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    ds.save_message("hi", "hi", 3)
    print("\n\n\n %s \n\n\n" % ds.get_history(3))

    return jsonify(result.data)


# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)


# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)


# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run server
if __name__ == '__main__':
    app.run(debug=True)

'''
