from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS 
from dotenv import load_dotenv

import os

load_dotenv()

database_url = "postgresql:" + ":".join(os.environ.get("DATABASE_URL", "").split(":")[1:])
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
CORS(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(144), nullable=False)
    meal = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)

    def __init__(self, title, price, description, meal, type, img):
        self.title = title
        self.price = price
        self.description = description
        self.meal = meal
        self.type = type
        self.img = img

class MenuItemSchema(ma.Schema):
    class Meta: 
        fields = ("id", "title", "price", "description", "meal", "type", "img")

menu_item_schema = MenuItemSchema()
multiple_menu_item_schema = MenuItemSchema(many=True)


@app.route('/menu-item/add', methods=["POST"])
def add_menu_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    price = post_data.get('price')
    description = post_data.get('description')
    meal = post_data.get('meal')
    type = post_data.get('type')
    img = post_data.get('img')

    item = db.session.query(MenuItem).filter(MenuItem.title == title).first()

    if title == None:
        return jsonify("Error: Data must have a 'title' key.")

    if price == None:
        return jsonify("Error: Data must have a 'price' key.")

    if description == None:
        return jsonify("Error: Data must have a 'description' key.")

    if meal == None:
        return jsonify("Error: Data must have a 'meal' key.")

    if type == None:
        return jsonify("Error: Data must have a 'type' key.")

    if img == None:
        return jsonify("Error: Data must have a 'img' key.")

    
    new_item = MenuItem(title, price, description, meal, type, img)
    db.session.add(new_item)
    db.session.commit()

    return jsonify("You've added a new menu item!")


@app.route('/menu-item/get', methods=["GET"])
def get_menu_items():
    items = db.session.query(MenuItem).all()
    return jsonify(multiple_menu_item_schema.dump(items))


@app.route('/menu-item/get/<id>', methods=["GET"])
def get_menu_item_by_id(id):
    item = db.session.query(MenuItem).filter(MenuItem.id == id).first()
    return jsonify(menu_item_schema.dump(item))


@app.route('/menu-item/delete/<id>', methods=["DELETE"])
def delete_menu_item(id):
    item = db.session.query(MenuItem).filter(MenuItem.id == id).first()
    db.session.delete(item)
    db.session.commit()

    return jsonify("The menu item has been deleted")


@app.route('/menu-item/update/<id>', methods=["PUT", "PATCH"])
def update_menu_item_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    price = post_data.get('price')
    description = post_data.get('description')
    meal = post_data.get('meal')
    type = post_data.get('type')
    img = post_data.get('img')

    item = db.session.query(MenuItem).filter(MenuItem.id == id).first()

    if title != None:
        item.title = title
    if price != None:
        item.price = price
    if description != None:
        item.description = description
    if meal != None:
        item.meal = meal
    if type != None:
        item.type = type
    if img != None:
        item.img = img

    db.session.commit()
    return jsonify("Menu item has been updated.")



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)

    def __init__(self, title, price, type, img):
        self.title = title
        self.price = price
        self.type = type
        self.img = img

class CartSchema(ma.Schema):
    class Meta: 
        fields = ("id", "title", "price", "type", "img")

cart_schema = CartSchema()
multiple_cart_schema = CartSchema(many=True)


@app.route('/cart/add', methods=["POST"])
def add_cart_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    price = post_data.get('price')
    type = post_data.get('type')
    img = post_data.get('img')

    item = db.session.query(Cart).filter(Cart.title == title).first()

    if title == None:
        return jsonify("Error: Data must have a 'title' key.")

    if price == None:
        return jsonify("Error: Data must have a 'price' key.")

    if type == None:
        return jsonify("Error: Data must have a 'type' key.")

    if img == None:
        return jsonify("Error: Data must have a 'img' key.")

    
    new_item = Cart(title, price, type, img)
    db.session.add(new_item)
    db.session.commit()

    return jsonify("You've added a new cart item!")


@app.route('/cart/get', methods=["GET"])
def get_cart_items():
    items = db.session.query(Cart).all()
    return jsonify(multiple_cart_schema.dump(items))


@app.route('/cart/get/<id>', methods=["GET"])
def get_cart_item_by_id(id):
    item = db.session.query(Cart).filter(Cart.id == id).first()
    return jsonify(cart_schema.dump(item))


@app.route('/cart/delete/<id>', methods=["DELETE"])
def delete_cart_item_by_id(id):
    item = db.session.query(Cart).filter(Cart.id == id).first()
    db.session.delete(item)
    db.session.commit()

    return jsonify("The cart item has been deleted")


@app.route('/cart/delete', methods=['DELETE'])
def delete_all_cart_items():
    all_cart_items = db.session.query(Cart).all()
    for item in all_cart_items:
        db.session.delete(item)
    
    db.session.commit()
    return jsonify('All your cart items have been deleted.')
    

if __name__ == "__main__":
    app.run(debug=True)