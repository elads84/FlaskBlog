from app import app, db
from app.models import User, Post, Comment, Like

if __name__ == '__main__':
    with app.app_context():
        user = User(username='Elad',
                    email="elad@mail.com")
        user.set_password('1234')
        db.session.add(user)
        db.session.commit()
        post = Post(
            title="Test Post",
            body="Test body",
            user_id=user.id
        )

        db.session.add(post)
        db.session.commit()
