from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import hashlib
import os


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256))
    profile_pic = db.Column(db.String(256),
                            default=os.path.join('static', 'profile_photos', 'default.jpg'))
    posts = db.relationship("Post", backref='author', lazy=True, order_by='Post.id.desc()')
    comments = db.relationship("Comment", backref='author', lazy=True)
    likes = db.relationship("Like", backref='author', lazy=True)

    def __str__(self):
        return f"{self.email}, {self.id}"

    def set_password(self, password: str) -> None:
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    has_photo = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship("Comment", backref='post', lazy=True, order_by="Comment.id.desc()")
    likes = db.relationship("Like", backref='post', lazy=True)

    def __str__(self):
        return f'{self.author.email}, {self.title}: {self.body}'

    def did_user_like(self, user_id):
        for like in self.likes:
            if like.user_id == user_id:
                return True
        return False


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    comment = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
