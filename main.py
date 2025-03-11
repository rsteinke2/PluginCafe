from flask import Flask, abort, render_template, redirect, url_for, flash
from sqlalchemy import Boolean, Float
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreateCafeForm, RegisterForm, LoginForm, CommentForm
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:  # Check if the user is not admin
            return abort(403)  # Forbidden

        return f(*args, **kwargs)

    return decorated_function

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    cafes = relationship("Cafe", back_populates="author")


class Cafe(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="cafes")
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return render_template("index.html", cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/cafe/<int:cafe_id>")
def show_cafe(cafe_id):
    # Retrieve a BlogPost from the database based on the post_id
    requested_cafe = db.get_or_404(Cafe, cafe_id)
    return render_template("cafe.html", cafe=requested_cafe)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    # Passing True or False if the user is authenticated.
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already registered with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/delete/<int:cafe_id>")
@admin_only
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/new-cafe", methods=["GET", "POST"])
@admin_only
def add_new_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            author=current_user,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data.lower() == 'true',  # Convert to Boolean
            has_wifi=form.has_wifi.data.lower() == 'true',  # Convert to Boolean
            has_sockets=form.has_sockets.data.lower() == 'true',  # Convert to Boolean
            can_take_calls=form.can_take_calls.data.lower() == 'true',  # Convert to Boolean
            coffee_price=form.coffee_price.data,
            rating=form.rating.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash("Your cafe has been created successfully!", "success")
        return redirect(url_for('home'))
    return render_template("make_cafe.html", form=form)

@app.route("/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
@admin_only
def edit_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    edit_form = CreateCafeForm(
        name=cafe.name,
        author=cafe.author,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        seats=cafe.seats,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        can_take_calls=cafe.can_take_calls,
        coffee_price=cafe.coffee_price,
        rating=cafe.rating
    )
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.author = current_user
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.seats = edit_form.seats.data
        cafe.has_toilet = edit_form.has_toilet.data.lower() == 'true'
        cafe.has_wifi = edit_form.has_wifi.data.lower() == 'true'
        cafe.has_sockets = edit_form.has_sockets.data.lower() == 'true'
        cafe.can_take_calls = edit_form.can_take_calls.data.lower() == 'true'
        cafe.coffee_price = edit_form.coffee_price.data
        cafe.rating = edit_form.rating.data
        db.session.commit()
        flash("Your cafe has been edited successfully!", "success")
        requested_cafe = db.get_or_404(Cafe, cafe_id)
        return render_template("cafe.html", cafe=requested_cafe)
    return render_template("make_cafe.html", form=edit_form, is_edit=True)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
