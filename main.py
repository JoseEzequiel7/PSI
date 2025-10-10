from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Livro, SessionLocal

bp = Blueprint('main' , __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/livros')
@login_required
def listar_livros():
    with SessionLocal() as session:
        user = session.query(User).where(User.id == current_user.id).first() 
        livros = user.livros if user else [] 
        return render_template('livros.html', livros=livros)
    
@bp.route('/livros/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano = request.form['ano']

        with SessionLocal() as session:
            with session.begin():
                livro = Livro(titulo=titulo, ano=ano, autor_id=current_user.id)
                session.add(livro)
                user = session.query(User).where(User.id == current_user.id).first()
                if user:
                    user.livros.append(livro) 

            flash('Livro adicionado com sucesso!', 'success')
            return redirect(url_for('main.listar_livros'))
    return render_template('livro_form.html', action='Adicionar')

@bp.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    with SessionLocal() as session:
        # Busca o livro dentro da sessão
        livro = session.get(Livro, id)
        
        # Otimização: Verifica se o livro existe e se o usuário logado é o autor_id
        if not livro or livro.autor_id != current_user.id:
            flash('Livro não encontrado ou você não tem permissão para editar.', 'danger')
            return redirect(url_for('main.listar_livros'))

        if request.method == 'POST':
            # 1. Atualiza os dados do objeto (que está anexado à sessão)
            livro.titulo = request.form['titulo']
            livro.ano = request.form['ano']
            
            # 2. CHAMA O COMMIT EXPLÍCITO para salvar as alterações
            session.commit() # <--- Novo Commit Adicionado
            
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('main.listar_livros'))
        
        return render_template('livro_form.html', action='Editar', livro=livro)
    
@bp.route('/livros/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_livro(id):
    with SessionLocal() as session:
        with session.begin():
            livro = session.query(Livro).where(Livro.id == id).first()
            
            if livro and livro.autor_id == current_user.id:
                session.delete(livro)
                flash('Livro excluído com sucesso!', 'success')
            else:
                flash('Livro não encontrado ou você não tem permissão para excluir.', 'danger')
                
        return redirect(url_for('main.listar_livros'))