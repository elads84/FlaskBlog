from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app.forms import LoginForm, SignUpForm, NewPostForm
from werkzeug.utils import secure_filename
from app.models import User, Post, Like, Comment
from app import app, db, login_manager
import os
from app.pic_editor import resize_image, create_image_name, set_photo, delete_file
from datetime import datetime


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Please log in to view this page', category='warning')
    return redirect(url_for('login'))


@app.route('/')
@app.route('/index')
@app.route('/home')
@login_required
def index():
    posts = Post.query.order_by(sa.desc(Post.id)).all()
    return render_template('index.html', title='My Blog 2024 💚', posts=posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('Login success', category='success')
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Wrong Login', category='danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login 💚', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash(f"Email {email} is already taken, Try a different one please!", category='danger')
            return redirect(url_for('signup'))
        elif username_exists:
            flash(f"Username {username} is already taken, Try a different one please!", category='danger')
            return redirect(url_for('signup'))
        else:
            user = User(email=email, username=username)
            user.set_password(form.password.data)
            file = form.image.data

            if file:
                user.profile_pic = set_photo(file, app, 'PROFILE_PIC_WIDTH', 'profile_photos')

            db.session.add(user)
            db.session.commit()
            flash('Successfully registered, Please log in 😊', category='success')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log out successfully', category='success')
    return redirect(url_for('login'))


@app.route('/edit/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit(post_id):
    edit_post = db.session.get(Post, post_id)
    posts = current_user.posts
    form = NewPostForm(title=edit_post.title, body=edit_post.body)

    if form.validate_on_submit():
        edit_post.title = form.title.data
        edit_post.body = form.body.data
        edit_post.timestamp = datetime.utcnow()

        file = form.image.data if form.image.data else None
        has_image = bool(file)

        if file:
            if edit_post.has_photo:
                delete_file(edit_post.photo)
            edit_post.photo = set_photo(file, app, 'POST_PIC_WIDTH', 'post_photos')
            edit_post.has_photo = has_image

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('new_post.html', edit_post=edit_post, posts=posts, form=form)


@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = db.session.get(Post, post_id)

    if post.has_photo:
        delete_file(post.photo)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    posts = current_user.posts
    form = NewPostForm()
    if form.validate_on_submit():
        user_id = current_user.id
        title = form.title.data
        body = form.body.data
        file = form.image.data if form.image.data else None
        has_image = bool(file)

        post = Post(
            title=title,
            body=body,
            has_photo=has_image,
            user_id=user_id,
        )

        if has_image:
            post.photo = set_photo(file, app, 'POST_PIC_WIDTH', 'post_photos')

        db.session.add(post)
        db.session.commit()

        return redirect('index')

    return render_template('new_post.html', form=form, posts=posts)


@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    liked = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if liked:
        db.session.delete(liked)
    else:
        like_ = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like_)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    comment = request.form.get('comment')
    new_comment = Comment(post_id=post_id, user_id=current_user.id, comment=comment)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_comment/<int:comment_id>', methods=['POST', 'GET'])
def edit_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if request.method == "GET":
        return render_template('edit_comment.html', comment=comment)

    else:
        comment.comment = request.form.get('comment_content')
        db.session.commit()
        return redirect(url_for('index'))
