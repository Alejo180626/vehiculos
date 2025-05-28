from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # clave para manejar sesiones

# Usuarios simulados con roles
usuarios = {
    "admin": {"password": "admin123", "rol": "administrador"},
    "consulta": {"password": "consulta123", "rol": "consulta"}
}


def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'administrador':
            return "Acceso denegado: Solo administradores", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        user = usuarios.get(usuario)
        if user and user['password'] == password:
            session['usuario'] = usuario
            session['rol'] = user['rol']
            return redirect(url_for('home'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_requerido
def home():
    return render_template('home.html')

@app.route('/registrar', methods=['GET', 'POST'])
@login_requerido
@admin_requerido
def registrar():
    if request.method == 'POST':
        placa = request.form['placa']
        tipo = request.form['tipo']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        celular = request.form['celular']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vehiculos (placa, tipo, nombres, apellidos, cedula, celular)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (placa, tipo, nombres, apellidos, cedula, celular))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('registrar.html')

@app.route('/vehiculos')
@login_requerido
@admin_requerido
def listar_vehiculos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT placa, tipo, nombres, apellidos, cedula, celular FROM vehiculos')
    vehiculos = cursor.fetchall()
    conn.close()
    return render_template('vehiculos.html', vehiculos=vehiculos)

@app.route('/buscar', methods=['GET', 'POST'])
@login_requerido
def buscar():
    resultado = None
    mensaje = None
    if request.method == 'POST':
        placa_buscar = request.form['placa']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT placa, tipo, nombres, apellidos, cedula, celular FROM vehiculos WHERE placa=?
        ''', (placa_buscar,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado is None:
            mensaje = "El vehículo no pertenece a la unidad."

    return render_template('buscar.html', resultado=resultado, mensaje=mensaje)

@app.route('/editar/<placa>', methods=['GET', 'POST'])
@login_requerido
@admin_requerido
def editar(placa):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        tipo = request.form['tipo']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        celular = request.form['celular']

        cursor.execute('''
            UPDATE vehiculos SET tipo=?, nombres=?, apellidos=?, cedula=?, celular=?
            WHERE placa=?
        ''', (tipo, nombres, apellidos, cedula, celular, placa))
        conn.commit()
        conn.close()
        return redirect('/vehiculos')

    cursor.execute('SELECT placa, tipo, nombres, apellidos, cedula, celular FROM vehiculos WHERE placa = ?', (placa,))
    vehiculo = cursor.fetchone()
    conn.close()
    return render_template('editar.html', vehiculo=vehiculo)

@app.route('/eliminar/<placa>')
@login_requerido
@admin_requerido
def eliminar(placa):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vehiculos WHERE placa = ?', (placa,))
    conn.commit()
    conn.close()
    return redirect('/vehiculos')


if __name__ == '__main__':
    app.run(debug=True)




