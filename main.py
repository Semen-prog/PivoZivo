from flask import Flask, render_template, request, redirect, session, g
from db_runner import exec
import json, os, shutil, firebase

app = Flask(__name__)

app.secret_key = "sdfDhny%v3cBX@^6C6ZqBEeq8!*as$3T%VZzEAU8"
main_topic = "info"

@app.route('/enter', methods=['POST', 'GET'])
def enter():
    isLogged = session.get("isLogged")
    if isLogged:
        return redirect('/')
    error = False
    if request.method == 'POST':
        password = request.form["password"]
        if password == firebase.get_secret():
            session["isLogged"] = True
            return redirect('/')
        error = True
    return render_template('enter.html', error=error)

@app.route('/')
def main():
    isLogged = session.get("isLogged")
    if not isLogged:
        return redirect('/enter')
    json = firebase.get_all()
    data = []
    for key, value in json.items():
        data.append((value["id"], value["name"], value["exists"], f"/change/{value['id']}", value["cost"]))
    return render_template('main.html', data=data)

@app.route('/logout')
def logout():
    session["isLogged"] = False
    return redirect('/enter')

@app.route('/changepass', methods=['GET', 'POST'])
def changepass():
    error = None
    isLogged = session.get("isLogged")
    if not isLogged:
        return redirect('/enter')
    if request.method == 'POST':
        old = request.form['old']
        new = request.form['new']
        repeat = request.form['repeat']
        if old != firebase.get_secret():
            error = 'Похоже, вы неправильно ввели старый пароль'
        elif new != repeat:
            error = 'Упс, пароли не совпадают'
        else:
            firebase.set_secret(new)
            return redirect('/enter')
    return render_template('changepass.html', error=error)

@app.route('/new', methods=['GET', 'POST'])
def new():
    isLogged = session.get("isLogged")
    if not isLogged:
        return redirect('/enter')
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']
        cost = request.form['cost']
        firebase.add_product(name, info, cost)
        return redirect('/')
    return render_template('new.html')

@app.route('/change/<int:id>', methods=['POST', 'GET'])
def change(id):
    isLogged = session.get("isLogged")
    if not (isLogged == True):
        return redirect('/enter')
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']
        exists = None
        try:
            checkBox = request.form['checkBox']
            exists = 1
        except:
            exists = 0
        cost = request.form['cost']
        d = {'id': id, 'name': name, 'info': info, 'cost': cost, 'exists': exists}
        firebase.update_product(d)
        return redirect('/')
    json = firebase.get(id)
    for key, value in json.items():
        data = (value["name"], value["info"], value["exists"], value["cost"])
    return render_template('change.html', info=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')