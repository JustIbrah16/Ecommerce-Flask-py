from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature
from flask_bootstrap import Bootstrap
from routes.categorias import categorias
from routes.productos import productos
from routes.pedidos import pedidos
from routes.usuarios import usuarios
from routes.main import main
from utils.db import db
from models.usuarios import Usuarios
from flask_login import LoginManager
from routes.permisos import permisos
from utils.permisos import tiene_permiso_filter
from utils.hash import hash_generator, check_password
from datetime import timedelta




app = Flask(__name__)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'

app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secret-password'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ecommerceflask@gmail.com'
app.config['MAIL_PASSWORD'] = 'rcte wjdz kswl haxi'
mail = Mail(app)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

db.init_app(app)

app.jinja_env.filters['tiene_permiso'] = tiene_permiso_filter

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('usuarios.login'))

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']

        if email and email.strip(): 
            user = Usuarios.query.filter_by(email=email).first()

            if user:  
                s = Serializer(app.config['SECRET_KEY'])
                token = s.dumps({'email': email}, salt='reset-password')
                reset_url = url_for('reset_password', token=token, _external=True)

                message = Message('Restablecimiento de contraseña',
                                  sender='no-reply@tuapp.com',
                                  recipients=[email])
                message.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}'
                mail.send(message)

                flash('Te hemos enviado un enlace para restablecer tu contraseña por correo electrónico', 'info')

                return redirect(url_for('usuarios.login'))

            else:
                flash('No encontramos ese correo electrónico en nuestros registros', 'error')
                return render_template('reset_request.html')  

        else:
            flash('Por favor ingresa un correo electrónico válido', 'error')
            return render_template('reset_request.html')  

    return render_template('reset_request.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='reset-password')['email']
    except (BadSignature):
        flash('El enlace ha expirado o es invalido', 'error')
        return redirect(url_for('reset_password_request'))
    
    user = Usuarios.query.filter_by(email = email).first()
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('reset_password_request'))
    
    if request.method == 'POST':
        new_password = request.form['password']

        hashed_password = hash_generator(new_password)
        user.password = hashed_password
        db.session.commit()
        flash('Tu contraseña ha sido restablecida exitosamente', 'success')
        return redirect(url_for('usuarios.login'))

    return render_template('reset_password.html', token = token)


app.register_blueprint(main)
app.register_blueprint(categorias)
app.register_blueprint(productos)
app.register_blueprint(pedidos)
app.register_blueprint(usuarios)
app.register_blueprint(permisos)

