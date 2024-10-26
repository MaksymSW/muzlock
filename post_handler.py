import random
import sqlite3
from datetime import date

from faker import Faker

faker = Faker()


def generate_post():
    user_id = random.randint(1, 10)
    created_at = faker.date_time()
    text = faker.text(100)
    is_publish = faker.boolean(chance_of_getting_true=50)
    return user_id, created_at, text, is_publish


def generate_file(user_id: int, created_at: date or str):
    type_id = random.randint(1, 3)
    link = faker.url()
    return user_id, type_id, link, created_at


def file_post_bind(user_id, created_at, conn):
    query = f"""
        SELECT pt.id, fl.id
        FROM posts AS pt
        JOIN files as fl
        ON pt.user_id = fl.user_id
        WHERE pt.user_id = {user_id} AND pt.created_at = '{created_at}'
        """
    print(query)
    result = conn.execute(query).fetchone()
    print(result)
    return result

def save_post_to_db():
    post = generate_post()
    file = generate_file(user_id=post[0], created_at=post[1])
    with sqlite3.connect('muzlock.db') as conn:
        script_post = """
        INSERT INTO posts (user_id, created_at, text, is_publish)
        VALUES (?, ?, ?, ?)
        """
        post_data = conn.execute(script_post, post)
        print(post_data)
        conn.commit()
        script_file = """
        INSERT INTO files (user_id, type_id, link, created_at)
        VALUES (?, ?, ?, ?)
        """
        file_data = conn.execute(script_file, file)
        print(file_data)
        conn.commit()
        ids_to_bind = file_post_bind(user_id=post[0], created_at=post[1], conn=conn)
        script_to_bind = """
        INSERT INTO files_posts (post_id, file_id)
        VALUES (?, ?)
        """
        conn.execute(script_to_bind, ids_to_bind)
        conn.commit()


if __name__ == "__main__":
    save_post_to_db()

