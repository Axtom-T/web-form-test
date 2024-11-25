#TODO: insert values for new tables and test displays
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
    type = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    FAT_status = db.Column(db.String)
    FAT_test_id = db.Column(db.Integer)
    SAT_status = db.Column(db.String)
    SAT_test_id = db.Column(db.Integer)
    SIAT_status = db.Column(db.String)
    SIAT_test_id = db.Column(db.Integer)
    FST_status = db.Column(db.String)
    FST_test_id = db.Column(db.Integer)
    project_number = db.Column(db.Integer)

class CCTV_SIAT_results(db.Model):
    __tablename__ = 'CCTV_SIAT_results'
    test_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer)
    test_date = db.Column(db.DateTime)
    pingable = db.Column(db.Boolean)
    ping_latency_expected = db.Column(db.Boolean)
    ping = db.Column(db.Integer)
    web_access = db.Column(db.Boolean)
    FLIR_discover = db.Column(db.Boolean)
    video_settings = db.Column(db.Boolean)
    focus = db.Column(db.Boolean)
    clean_display = db.Column(db.Boolean)
    picture_quality = db.Column(db.Boolean)
    PTZ_function = db.Column(db.Boolean)
    PTZ_privacy = db.Column(db.Boolean)
    washer = db.Column(db.Boolean)
    preset = db.Column(db.Boolean)
    recording = db.Column(db.Boolean)
    webcam_position = db.Column(db.Boolean)
    firmware_version = db.Column(db.String)
    record_diagnostics = db.Column(db.Boolean)
    SIAT_pass = db.Column(db.String)

@app.route('/')
def index():
   print('Request for index page received')
   try:
    devices = db.session.execute(db.select(Devices)).scalars().all()
    return render_template('index.html', devices=devices)
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
