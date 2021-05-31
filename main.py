import datetime
import os

from flask import (Flask, render_template, redirect, request, abort)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)

from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from forms.user import LoginForm, RegisterForm
from blueprints.news import blueprint_news
from blueprints.users import blueprint_users
from blueprints.comments import blueprint_comments
from blueprints.admin import blueprint_admin

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'Matskepladze_Yanochkin2004!'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['FLASK_DEBUG'] = 0

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(blueprint_news, url_prefix='/news')
app.register_blueprint(blueprint_users, url_prefix='/user')
app.register_blueprint(blueprint_comments, url_prefix='/comments')
app.register_blueprint(blueprint_admin, url_prefix='/admin')


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error, message=''):
    return render_template('nothing.html', message=message)


@app.errorhandler(405)
def not_found(error):
    return render_template('nothing.html')


@app.route("/")
def index():
    db_sess = create_session()
    if request.args.get('my') and current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user_id == current_user.id))
    elif current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    news = sorted(news, key=lambda x: x.created_date, reverse=True)
    return render_template("index.html", news=news, title='Новости')


@app.route('/messages')
@login_required
def messages():
    db_sess = create_session()
    if current_user.is_authenticated:
        ns = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        ns = db_sess.query(News).filter(News.is_private != True)
    return render_template("messages.html", news=ns, title='messages')


@app.route('/about_us')
def about_us():
    return render_template("about_us.html", title='о нас')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть (имя)")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            instrument=form.instrument.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    global_init("db/blogs.db")

    port = int(os.environ.get("PORT", 8080))
    app.run(port=port)  # host='0.0.0.0'
