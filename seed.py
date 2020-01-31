from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add dummy users
whiskey = User(first_name='Whiskey', last_name='Lane', img_url='https://www.rithmschool.com/assets/team/whiskey-4afaa4064090599efd8501e7693464d3968d036a0b683407611c746a9e4d732a.jpg')
nicholai = User(first_name='Nicholai', last_name='Hansen')
james = User(first_name='James', last_name='Ng')
deleted = User(first_name='Useless', last_name='POS')

# Add dummy posts
whiskey_post = Post(title='I\'m a dog', content='woof', user_id=1)
james_post = Post(title='Testing', content='Paragraph', user_id=3)

# Add new users to session
db.session.add(whiskey)
db.session.add(nicholai)
db.session.add(james)

# Add new posts
db.session.add(whiskey_post)
db.session.add(james_post)

# Commmit
db.session.commit()
