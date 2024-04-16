from flask import Flask, request, jsonify, render_template, redirect, session
import redis
import os
import uuid
import dotenv

dotenv.load_dotenv(".flaskenv")

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

@app.route('/new', methods=['GET'])
def new():
    if is_logged():
        return render_template('createTuip.html')
    else:
        return redirect('/login')
    
@app.route('/deletedb', methods=['GET'])
def deletedb():
    if is_logged():
        r.flushdb()
        session.pop('user', None)
        
    return redirect('/login')
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
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    session.pop('user', None)
    return jsonify({'message': 'Cierre de sesión exitoso'}), 200

@app.route('/api/tuips', methods=['GET'])
def api_tuips():
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    tuip_keys = r.keys('tuips:*')
    tuips = []
    for tuip_key in tuip_keys:     
        tuip = r.hgetall(tuip_key)
        tuip['likes'] = r.scard(f'likes:{tuip_key.split(":")[1]}')
        tuip['like'] = session.get('user') in r.smembers(f'likes:{tuip_key.split(":")[1]}')
        tuips.append({'id': tuip_key.split(':')[1], **tuip})
    tuips.sort(key=lambda x: int(x['id']), reverse=True)
    return jsonify(tuips), 200


@app.route('/api/tuips', methods=['POST'])
def api_tuip():
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    try:
        title = request.get_json()['title']
        content = request.get_json()['content']
        author = session.get('user')
        
        tuip_id = r.incr('tuip_id')
        
        r.hmset(f'tuips:{tuip_id}', {'title': title, 'content': content, 'author': author})
    except:
        return jsonify({'message': 'Error al crear tuip'}), 500
    return jsonify({'message': 'Tuip creado exitosamente'}), 201

@app.route('/api/tuips/<id>', methods=['GET'])
def api_get_tuip(id):
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    tuip = r.hgetall(f'tuips:{id}')
    if tuip:
        tuip = {k.decode('utf-8'): v.decode('utf-8') for k, v in tuip.items()}
        tuip['like'] = session.get('user') in r.smembers(f'likes:{id}')
        tuip['likes'] = r.scard(f'likes:{id}')
        return jsonify({'id': id, **tuip}), 200
    else:
        return jsonify({'message': 'Tuip no encontrado'}), 404
    
@app.route('/api/tuips/<id>', methods=['DELETE'])
def api_delete_tuip(id):
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    if r.exists(f'tuips:{id}'):
        propietary = r.hget(f'tuips:{id}', 'author').decode('utf-8')
        if propietary == session.get('user'):
            r.delete(f'tuips:{id}')
            return jsonify({'message': 'Tuip eliminado exitosamente'}), 200
        else:
            return jsonify({'message': 'No tienes permisos para eliminar este tuip'}), 403
    else:
        return jsonify({'message': 'Tuip no encontrado'}), 404

@app.route('/api/like/<id>', methods=['POST'])
def api_like(id):
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    if r.exists(f'tuips:{id}'):
        user = session.get('user')
        if not r.sismember(f'likes:{id}', user):
            r.sadd(f'likes:{id}', user)
            return jsonify({'message': 'Like agregado exitosamente'}), 200
        else:
            return jsonify({'message': 'Ya has dado like a este tuip'}), 409
    else:
        return jsonify({'message': 'Tuip no encontrado'}), 404
    
@app.route('/api/like/<id>', methods=['DELETE'])
def api_dislike(id):
    if not is_logged():
        return jsonify({'message': 'No hay una sesión activa'}), 404
    if r.exists(f'tuips:{id}'):
        user = session.get('user')
        if r.sismember(f'likes:{id}', user):
            r.srem(f'likes:{id}', user)
            return jsonify({'message': 'Like eliminado exitosamente'}), 200
        else:
            return jsonify({'message': 'No has dado like a este tuip'}), 409
    else:
        return jsonify({'message': 'Tuip no encontrado'}), 404

@app.route('/api/like/<id>/blast', methods=['POST'])
def api_blast(id):
    # This method does not need to check if the user is logged in, just like the tuip as a blast user to test concurrency
    if r.exists(f'tuips:{id}'):
        user = str(uuid.uuid4())
        r.sadd(f'likes:{id}', user)
        return jsonify({'message': 'Like agregado exitosamente'}), 200
    else:
        return jsonify({'message': 'Tuip no encontrado'}), 404
    
    

