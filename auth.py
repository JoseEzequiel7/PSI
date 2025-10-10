from flask import Blueprint , render_template , request , redirect , url_for , flash
from flask_login import login_user , logout_user , login_required
from models import User , SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth' , __name__ , url_prefix='/')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['senha'].strip()

        with SessionLocal() as session: 
            if session.query(User).where(User.email == email).first():
                flash('Nome de usuário já está em uso.', 'warning')
                return redirect(url_for('auth.register')) 

            hashed_password = generate_password_hash(password)
            novo_user = User(email=email, password=hashed_password)
            session.add(novo_user)

            session.commit()
                        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login')) 
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['senha'].strip()

        with SessionLocal() as session:
            with session.begin():
                user = session.query(User).where(User.email == email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('main.listar_livros')) 
            else:
                flash('Usuário ou senha incorretos.', 'danger')
                return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))