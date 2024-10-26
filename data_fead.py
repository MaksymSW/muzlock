from faker import Faker
import random
import sqlite3

faker = Faker()


def generate_users(user_count: int):
    users = []

    for i in range(user_count):
        role_id = random.randint(1, 3)
        full_name = faker.name()
        phone = faker.phone_number()
        email = faker.email()
        location_id = random.randint(1, 3)
        created_at = faker.date()
        update_at = created_at
        users.append((role_id, full_name, phone, email, location_id, created_at, update_at))
    return users

def fill_users(users:list[tuple]):
    with sqlite3.connect('muzlock.db') as conn:
        script = """
        INSERT INTO users (role_id, fullname, phone, email, location_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        conn.executemany(script, users)
        conn.commit()
        print("table users was filled")

if __name__ == "__main__":
    users = generate_users(10)
    fill_users(users)
