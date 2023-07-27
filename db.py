from sqlalchemy import create_engine, text, insert
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
db_connection_string = os.getenv('DB_CONNECTION_STRING')


engine = create_engine(db_connection_string)



def load_users_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))

        all_users = []
        for row in result.all():
            all_users.append(dict(row))
            print(row)
        return all_users
    
def get_user_firstname_from_db(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = '%s'" %email))
        user = []
        for row in result.mappings().all():
            user.append(dict(row))
        user_firstname = user[0].get('firstname')
        return user_firstname
# result = get_user_firstname_from_db('jimh01@gmail.com')
# print(get_user_firstname_from_db('jimh01@gmail.com'))
# print(load_users_from_db())

def get_username_from_db(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = '%s'" %email))
        user = []
        for row in result.mappings().all():
            user.append(dict(row))
        username = user[0].get('username')
        return username
    

def get_password_from_db(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = '%s'" %email))
        user = []
        for row in result.mappings().all():
            user.append(dict(row))
        password = user[0].get('password')
        return password


def add_video_from_db(username, video_name, exercise_type):
    with engine.connect() as conn:
        query = text("INSERT INTO uploaded_videos (username, video_name, exercise_type) values ('%s', '%s', '%s')" %(username, video_name, exercise_type))
        conn.execute(query)
        result = conn.execute(text("SELECT * FROM uploaded_videos WHERE username = '%s'" %username))
        all_videos = []
        for row in result.mappings().all():
            all_videos.append(dict(row))
            print(row)
        return all_videos
    
def get_user(username):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM uploaded_videos WHERE username = '%s' ORDER BY upload_time DESC" %username))
        all_videos = []
        for row in result.mappings().all():
            all_videos.append(dict(row))
            print(row)
        return all_videos
    

def user_register(username, firstname, email, password):
    with engine.connect() as conn:
        query = text("INSERT INTO users (username, firstname, email, password ) values (:username, :firstname, :email, :password)")
        conn.execute(query, username=username, firstname=firstname, email=email, password=password)
    return "success"


def update(video_name, time):
    with engine.connect() as conn:
        iwantupdate = "UPDATE uploaded_videos SET timesdone = %s WHERE video_name = '%s'"%(time, video_name)
        query = text(iwantupdate)
        conn.execute(query)
    return time
