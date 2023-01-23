import json

from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:/Users/user/Documents/IT/shop/site/pivozivo-5eca7-firebase-adminsdk-44zqf-4e5602a883.json")
firebase_app = firebase_admin.initialize_app(cred)

base_ref = db.reference(url='https://pivozivo-5eca7-default-rtdb.firebaseio.com/', app=firebase_app)

def init():
    ref = base_ref
    with open("init_data.json") as f:
        data = json.load(f)
    ref.set(data)

def get(id):
    ref = base_ref.child("products")
    return ref.order_by_child("id").equal_to(id).get()

def get_secret():
    return base_ref.child("service").get()["secret_code"]

def set_secret(new):
    base_ref.child("service").update({"secret_code": new})

def get_all():
    ref = base_ref.child("products")
    return ref.get()

def update_product(d):
    ref = base_ref.child("products")
    list = ref.get()
    for key, value in list.items():
        if value["id"] == d["id"]:
            ref.child(key).update(d)
            return

def add_product(name, info, cost):
    indexes = base_ref.child("newid").get()
    id = dict(indexes)["products"]
    json = {'id': id, 'name': name, 'info': info, 'cost': cost, 'exists': 1}
    base_ref.child("products").push(json)
    base_ref.child("newid").update({"products": id + 1})