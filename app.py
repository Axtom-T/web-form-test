import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/menu', methods=['POST'])
def menu():
   func = request.form.get('Function')

   if func:
       print('Request for menu page received with function=%s' % func)
       return render_template('menu.html', name = func)
   else:
       print('Request for menu page received with no function or blank -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
