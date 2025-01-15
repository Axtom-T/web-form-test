#TODO: fix write to db functionality - id auto_incrementing
# implement actual routing according to design
#display db elements with CSS
import os
from flask_migrate import Migrate
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, session)
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from datetime import date

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
    test_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_id = db.Column(db.Integer)
    test_date = db.Column(db.DateTime)
    pingable = db.Column(db.String)
    ping_latency_expected = db.Column(db.String)
    ping = db.Column(db.Integer)
    web_access = db.Column(db.String)
    FLIR_discover = db.Column(db.String)
    video_settings = db.Column(db.String)
    focus = db.Column(db.String)
    clean_display = db.Column(db.String)
    picture_quality = db.Column(db.String)
    PTZ_function = db.Column(db.String)
    PTZ_privacy = db.Column(db.String)
    washer = db.Column(db.String)
    preset = db.Column(db.String)
    recording = db.Column(db.String)
    webcam_position = db.Column(db.String)
    firmware_version = db.Column(db.String)
    record_diagnostics = db.Column(db.String)
    SIAT_pass = db.Column(db.String)

    def __init__(self, asset_id, test_date, pingable, ping_latency_expected, ping, web_access, FLIR_discover, video_settings,\
                 focus, clean_display, picture_quality, PTZ_function, PTZ_privacy, washer, preset, recording, webcam_position,\
                 firmware_version, record_diagnostics, SIAT_pass):
      self.asset_id = asset_id
      self.test_date = test_date
      self.pingable = pingable
      self.ping_latency_expected = ping_latency_expected
      self.ping = ping
      self.web_access = web_access
      self.FLIR_discover = FLIR_discover
      self.video_settings = video_settings
      self.focus = focus
      self.clean_display = clean_display
      self.picture_quality = picture_quality
      self.PTZ_function = PTZ_function
      self.PTZ_privacy = PTZ_privacy
      self.washer = washer
      self.preset = preset
      self.recording = recording
      self.webcam_position = webcam_position
      self.firmware_version = firmware_version
      self.record_diagnostics = record_diagnostics
      self.SIAT_pass = SIAT_pass

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    # build string in format 01-01-2000
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return date_string

@app.route('/')
def index():
   try:
    return render_template('index.html')
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text


@app.route('/hello', methods=['POST'])
def hello():
   try:
    name = request.form.get('name')
    session['name'] = name
    if name:
        return render_template('hello.html', template_name = name)
    else:
        return redirect(url_for('index'))
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text

@app.route('/menu', methods=['POST'])
def menu():
   try:
    project = request.form.get('proj')
    session['proj'] = project
    user = session.get('name')
    if project:
        return render_template('menu.html', template_project = project, template_user = user)
    else:
        return redirect(url_for('index'))
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text

@app.route('/testing', methods=['POST'])
def testing():
   try:
    user = session.get('name')
    project = session.get('proj')
    return render_template('testing.html',template_project = project, template_user = user)
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text

@app.route('/scheduling', methods=['POST'])
def scheduling():
   try:
    user = session.get('name')
    project = session.get('proj')
    return render_template('scheduling.html', template_user = user, template_project = project)
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text

@app.route('/stage', methods=['POST'])
def stage():
   try:
    user = session.get('name')
    project = session.get('proj')
    device = request.form.get('device')
    session['device'] = device
    return render_template('stage.html', template_user = user, template_project = project, template_device = device)
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text

@app.route('/CCTV_SIAT', methods=['POST'])
def CCTV_SIAT():
   try:
    user = session.get('name')
    project = session.get('proj')
    device = session.get('device')
    return render_template('CCTV_SIAT.html', template_user = user, template_project = project, template_device = device)
   except Exception as e:
    error_text = "<p>The error:<br>" + str(e) + "</p>"
    return error_text

@app.route('/add_record_CCTV_SIAT', methods = ['GET','POST'])
def add_record_CCTV_SIAT():
    try:
        asset_id = session.get('device')
        test_date = stringdate()
        pingable = request.form.get('pingable')
        ping_latency_expected = request.form.get('ping_latency_expected')
        ping = request.form.get('ping')
        web_access = request.form.get('web_access')
        FLIR_discover = request.form.get('FLIR_discover')
        video_settings = request.form.get('video_settings')
        focus = request.form.get('focus')
        clean_display = request.form.get('clean_display')
        picture_quality = request.form.get('picture_quality')
        PTZ_function = request.form.get('PTZ_function')
        PTZ_privacy = request.form.get('PTZ_privacy')
        washer = request.form.get('washer')
        preset = request.form.get('preset')
        recording = request.form.get('recording')
        webcam_position = request.form.get('webcam_position')
        firmware_version = request.form.get('firmware_version')
        record_diagnostics = request.form.get('record_diagnostics')
        SIAT_pass = request.form.get('SIAT_pass')
        record = CCTV_SIAT_results(asset_id,test_date,pingable,ping_latency_expected,ping,web_access,FLIR_discover,video_settings,\
                                    focus,clean_display,picture_quality,PTZ_function,PTZ_privacy,washer,preset,recording,webcam_position,\
                                    firmware_version,record_diagnostics,SIAT_pass)
        db.create_all()
        db.session.add(record)
        db.session.commit()
        msg = f"Data for device {asset_id} added"
        return render_template("add_record_CCTV_SIAT.html", template_msg = msg)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        return error_text   

@app.route('/display_tables',methods=['GET', 'POST'])
def display_tables():
    try:
        devices = db.session.execute(db.select(Devices)).scalars().all()
        cctv_siat = db.session.execute(db.select(CCTV_SIAT_results)).scalars().all()
        return render_template('display_tables.html', template_devices = devices, template_cctv_siat = cctv_siat)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        return error_text

if __name__ == '__main__':
   app.run()
