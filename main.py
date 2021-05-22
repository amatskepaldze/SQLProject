import datetime
import os

from flask import (Flask, render_template, redirect, request, abort)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from flask_restful import abort, Api

from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from forms.news import NewsForm, Response
from forms.user import LoginForm, RegisterForm, EditProfile

app = Flask(__name__)
app.config['SECRET_KEY'] = '42'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['FLASK_DEBUG'] = 0
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return render_template('nothing.html')


@app.errorhandler(405)
def not_found(error):
    return render_template('nothing.html')


@app.route("/")
def index():
    db_sess = create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/messages')
def messages():
    db_sess = create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("messages.html", news=news)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfile()
    db_sess = create_session()
    if form.validate_on_submit():
        print(1000)
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('profile.html', form=form,
                                   message="Такой пользователь уже есть")

        user = db_sess.query(User).filter(User.name == current_user.name).first()
        user.name = form.name.data
        user.about = form.about.data
        db_sess.commit()
        return redirect('/profile')
    form.name.data = current_user.name
    form.about.data = current_user.about

    return render_template('profile.html', form=form)


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
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
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
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('edit_news.html', title='Добавление новости', form=form)


@app.route('/news/<int:id>')
@login_required
def news(id):
    db_sess = create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news.is_private and news.user_id != current_user.id:
        return abort(405)
    return render_template('news.html', title=news.title, item=news)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_news.html', title='Редактирование новости', form=form)


@app.route('/response/<int:id>', methods=['GET', 'POST'])
@login_required
def response(id):
    form = Response()
    db_sess = create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if form.validate_on_submit():
        if news.is_private and news.user_id != current_user.id:
            return abort(405)
        #  дописать
        return redirect('/')  # если хочешь напиши все успешно
    return render_template('login.html', title='Отозваться', form=form, news_title=news.title)


def main():
    print('hello')
    global_init("db/blogs.db")
    # app.register_blueprint(news_api.blueprint)

    port = int(os.environ.get("PORT", 8080))
    app.run(port=port)
    '''
    user = db_sess.query(User).filter(User.id == 1).first()

    for news in user.news:
        print(news)'''


if __name__ == '__main__':
    main()
