#TODO: fix DB connection issue
import os
from flask_migrate import Migrate
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, session)
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
app.secret_key = 'placeholder'

server = os.getenv('AZURE_SQL_SERVER')
database = os.getenv('AZURE_SQL_DATABASE')
username = os.getenv('AZURE_SQL_DB_USER')
password = os.getenv('AZURE_SQL_DB_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

@app.route('/')
def index():
   print('Request for index page received')
   #return render_template('index.html')
   try:
    devices = db.session.execute(db.select(Devices)).scalars().all()
    device_txt = '<ul>'
    for i in devices:
        device_txt += '<li>' + str(i.id) + ', ' + i.description + '</li>'
    device_txt += '</ul>'
    return device_txt
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text


@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')
   session['name'] = name
   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/menu', methods=['POST'])
def menu():
   func = request.form.get('proj')
   user = session.get('name')
   if func:
       print('Request for menu page received with proj=%s' % func)
       return render_template('menu.html', name = func, user = user)
   else:
       print('Request for menu page received with no proj or blank -- redirecting')
       return redirect(url_for('index'))

@app.route('/function', methods=['POST'])
def function():
   tst = request.form.get('tst')

   if tst:
       print('Request for menu page received with tst=%s' % tst)
       return render_template('function.html', name = tst)
   else:
       print('Request for menu page received with no tst or blank -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()
