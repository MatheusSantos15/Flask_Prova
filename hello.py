import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuração do diretório base
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando as extensões
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos de banco de dados

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(250))

    def __repr__(self):
        return f'<Course {self.name}>'

# Formulários

class CourseForm(FlaskForm):
    name = StringField('Qual é o seu curso?', validators=[DataRequired()])
    description = TextAreaField('Descrição (250 caracteres)', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Cadastrar')

# Contexto de shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Course=Course)

# Tratamento de erros
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Rotas

@app.route('/', methods=['GET', 'POST'])
def index():
    nome = session.get('Matheus Santos do Nascimento')
    prontuario = "PT3026001"  # Substitua com seu prontuário real, se necessário.
    return render_template('index.html')

@app.route('/curso', methods=['GET', 'POST'])
def curso():
    form = CourseForm()
    courses = Course.query.all()

    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('curso'))  # Redireciona para a mesma página

    return render_template('curso.html', form=form, courses=courses)

@app.route('/indisponivel')
def indisponivel():
    return render_template('indisponivel.html')

# Iniciando a aplicação
