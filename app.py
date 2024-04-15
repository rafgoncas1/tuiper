from flask import Flask, request, jsonify, render_template, redirect, session
import redis
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def is_logged():
    if session.get('user'):
        return True
    else:
        return False

@app.route('/')
def index():
    if is_logged():
        return render_template('index.html')
    else:
        return redirect('/login')
    
@app.route('/login', methods=['GET'])
def login():
    if is_logged():
        return redirect('/')
    else:
        return render_template('login.html', navbar=False)

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html', navbar=False)
    
### API Routes ###

@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    if r.get(username) == password:
        session['user'] = username
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'message': 'Credenciales incorrectas'}), 404
    
@app.route('/api/register', methods=['POST'])
def api_register():
    username = request.get_json()['username']
    password = request.get_json()['password']
    if r.get(username):
        return jsonify({'message': 'El nombe de usuario ya existe'}), 409
    else:
        r.set(username, password)
        return jsonify({'message': 'Registro exitoso'}), 200
    
@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'message': 'Cierre de sesión exitoso'}), 200
