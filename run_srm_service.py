# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template
from flask import flash
from servmoncode import get_objects
from servmoncode import monitoring_process
from servmoncode import edit_db
from servmoncode import add_data_in_db
from servmoncode import delete_data_from_db
from servmoncode import edit_settings
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#get all settings, login/password(users) from db as dicts 

#get all receivers from db as objects
list_of_objects = get_objects.get_objects_receivers("active_only")

"""  New process that update objects  """
monitoring_process.start(list_of_objects)

@app.route('/')
def index():
    time = datetime.datetime.now().strftime("%H:%M")
    return render_template('index.html', name='Main', time=time)

@app.route('/satellite/<satellite>')
def monitoring(satellite):
    name = satellite
    time = datetime.datetime.now().strftime("%H:%M")
    final_list = get_data(name)
    return render_template('index.html', name = name, time=time, final_list = final_list)
    
@app.route('/receivers', methods=['POST', 'GET'])
def receivers():
    time = datetime.datetime.now().strftime("%H:%M")
    list_of_receivers = get_objects.get_objects_receivers("all")
    return render_template('index.html', name='Receivers', time=time, list_of_receivers=list_of_receivers)

@app.route('/add', methods=['POST'])
def add():
    status = add_data_in_db.add_data(request.form['ip'], request.form['model'], request.form['satellite'], request.form['login'], request.form['password'], request.form['port'], request.form['state'])
    flash(status)
    # add to the active list of receivers
    if status == "IP address and port have been added" and request.form['state'] == "used":
        obj = get_objects.return_object(request.form['ip'], request.form['model'], request.form['satellite'], request.form['login'], request.form['password'], request.form['port'], 1)
        list_of_objects.append(obj)
    return redirect(url_for('receivers'))

@app.route('/edit/<ip>/<port>/<action>',  methods=['POST', 'GET'])
def edit(ip, port, action):
    status = ""
    time = datetime.datetime.now().strftime("%H:%M")

    if action == "get":
        # receiver is dict -> keys: ip, model, satellite, login, password, port, state
        receiver = edit_db.select_receiver_for_edit(ip, port)
        return render_template('index.html', name='Edit', time=time, receiver=receiver)
    if action == "update":
        print(ip, request.form['model'], request.form['satellite'], request.form['login'], request.form['password'], port, request.form['state'])
        # update db
        status = edit_db.update_receiver(ip, request.form['model'], request.form['satellite'], request.form['login'], request.form['password'], port, request.form['state'])
        # check used or not
        # if used -> check in list_of_objects -> if exist -> remove, make obj and add-> if not -> make obj and add
        if request.form['state'] == "used":
            for obj in list_of_objects:
                if obj.ip == ip and obj.port == port:
                    list_of_objects.remove(obj)
            obj = get_objects.return_object(ip, request.form['model'], request.form['satellite'], request.form['login'], request.form['password'], port, 1)
            list_of_objects.append(obj)
        # if don't used -> check in list_of_objects -> if exist -> remove obj from list_of_objects
        elif request.form['state'] == "don't used":
            for obj in list_of_objects:
                if obj.ip == ip and obj.port == port:
                    list_of_objects.remove(obj)
        flash(status)
        return redirect(url_for('receivers'))
    if action == "delete":
        status = delete_data_from_db.delete_data(ip, port)
        flash(status)
        if status == "IP address and port have been removed":
            for obj in list_of_objects:
                if obj.ip == ip and obj.port == port and obj.state == 1:
                    list_of_objects.remove(obj)
        return redirect(url_for('receivers'))

@app.route('/settings')
def settings():
     time = datetime.datetime.now().strftime("%H:%M")
     return render_template('index.html', name='Settings', time=time)

def get_data(name):
    new_list = []
    for i in list_of_objects:
        if i.satellite == name:
            new_list.append(i)
    return new_list
