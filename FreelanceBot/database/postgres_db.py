import psycopg2
from create_bot import bot
import os
from dotenv import load_dotenv

load_dotenv()

def sql_start():
    global conn, cur
    conn = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASS'))
    cur = conn.cursor()

    if conn:
        print('Database connected successfully')


# User
async def add_user(message):
    cur.execute('insert into users (first_name, last_name, username, telegram_id) values (%s, %s, %s, %s)', (str(message.from_user.first_name), str(message.from_user.last_name), str(message.from_user.username), str(message.from_user.id)))
    conn.commit()

    print("[INFO] New user has been added!")


async def get_user_id(telegram_id):
    cur.execute('select id from users where telegram_id = %s', (str(telegram_id),))
    record = cur.fetchone()

    return record[0]


async def check_user(id):
    cur.execute('select exists(select 1 from users where telegram_id = %s)', (str(id),))
    records = cur.fetchone()

    return records[0]


async def get_user_status(tg_id):
    cur.execute('select status from users where telegram_id = %s', (str(tg_id),))
    record = cur.fetchone()

    return record[0]


async def set_user_status(user_id):
    cur.execute('update users set status = 0 where id = %s', (user_id,))
    conn.commit()

    print("[INFO] User status has been changed!")


async def set_moderator_status(username):
    cur.execute('update users set status = 1 where username = %s', (username,))
    conn.commit()

    print("[INFO] User status has been changed!")


async def get_telegram_users_id():
    cur.execute('select telegram_id from users');
    records = cur.fetchall()

    users_id = []

    for record in records:
        users_id.append(record[0])

    return users_id


async def get_list_of_moderators():
    cur.execute('select id, first_name, last_name, username from users where status = 1')
    records = cur.fetchall()

    return records


# Category
async def get_category_names():
    cur.execute('select name from categories')
    records = cur.fetchall()

    categories = []

    for record in records:
        categories.append(record[0])

    return categories


async def get_category_id(name):
    cur.execute('select id from categories where name = %s', (name,))
    record = cur.fetchone()

    return record[0]


# Advert
async def add_advert(data, user_id):
    cur.execute('insert into adverts (title, description, category_id, deadline, price, contacts, user_id) values (%s, %s, %s, %s, %s, %s, %s)', (data[0], data[1], data[2], data[3], data[4], data[5], user_id))
    conn.commit()

    print("[INFO] New advert has been added!")


async def delete_advert(advert_id):
    # here we just hide advert
    cur.execute('delete from adverts where id = %s', (advert_id,))
    conn.commit()

    print("[INFO] advert has been deleted!")


async def soft_delete_advert(advert_id):
    # here we just hide advert
    cur.execute('update adverts set is_hidden = True where id = %s', (advert_id,))
    conn.commit()

    print("[INFO] advert has been soft deleted!")


async def set_verified(advert_id):
    cur.execute('update adverts set is_verified = true where id = %s', (advert_id,))
    conn.commit()

    print('[INFO] Advert verified')


async def get_adverts():
    cur.execute('select adverts.title, adverts.description, categories.name, adverts.deadline, adverts.price, adverts.contacts from adverts inner join categories on adverts.category_id = categories.id where is_verified = True and is_hidden = False')
    records = cur.fetchall()

    return records


async def get_unverified_adverts():
    # cur.execute('select adverts.id, adverts.title, adverts.description, categories.name, adverts.deadline, adverts.price, adverts.contacts from adverts inner join categories on adverts.category_id = categories.id where is_verified = False and is_hidden = False')
    cur.execute('select adverts.id, adverts.title, adverts.description, categories.name, adverts.deadline, adverts.price, adverts.contacts, users.telegram_id from adverts inner join categories on adverts.category_id = categories.id inner join users on adverts.user_id = users.id where is_verified = False and is_hidden = False')
    records = cur.fetchall()

    return records


async def get_activ_adverts():
    cur.execute('select adverts.id, adverts.title, adverts.description, categories.name, adverts.deadline, adverts.price, adverts.contacts from adverts inner join categories on adverts.category_id = categories.id where is_verified = True and is_hidden = False')
    records = cur.fetchall()

    return records


async def get_my_adverts(user_id):
    cur.execute('select adverts.id, adverts.title, adverts.description, categories.name, adverts.deadline, adverts.price, adverts.contacts, adverts.is_verified from adverts inner join categories on adverts.category_id = categories.id where user_id = %s and is_hidden = False', (user_id,))
    records = cur.fetchall()

    return records



"""
    Users
    ---------
    id
    first_name 
    last_name
    username
    phone_number
    email
    status {
        - 0 user
        - 1 moderator
    }
    telegram_id
    created_at
    
    # SQL 
    create table users (
        id serial primary key,
        first_name text,
        last_name text, 
        username text,
        phone_number text,
        email text,
        status int default 0,
        telegram_id text,
        created_at timestamp default current_timestamp
    );
    
     create table users (id serial primary key, first_name text, last_name text, username text, phone_number text, email text, status int default 0, telegram_id text, created_at timestamp default current_timestamp);
    
    
    Adverts 
    ----------
    id 
    title 
    description
    category_id
    deadline 
    price 
    contacts
    is_verified True/Fasle default Fasle 
    user_id 
    created_at
    is_hidden boolean default fasle
    
    
    create table adverts (
        id serial primary key,
        title text,
        description text,
        category_id int,
        deadline text,
        price text,
        contacts text,
        is_verified boolean default fasle,
        user_id int
        created_at timestamp default current_timestamp,
        is_hidden boolean default fasle
    )
    
    create table adverts (id serial primary key, title text, description text, category_id int, deadline text, price text, contacts text, is_verified boolean default FALSE, user_id int, is_hidden boolean default fasle);
    
    Categories
    -----------
    id 
    name
    
    create table categories (
        id serial primary key,
        name text
    );
    
    create table categories (id serial primary key, name text);
    
    insert into categories (name) values ('Дизайн и Арт'), ('Тексты'), ('Программирование'), ('Аудио/Видео'), ('Разработка игр'), ('Реклама и Маркетинг'), ('Аутсорсинг и консалтинг'), ('Анимация и флеш'), ('3D Графика'), ('Фотография'), ('Инжиниринг'), ('Архитектура/Интерьер'), ('Оптимизация (SEO)'), ('Полиграфия'), ('Обучение и консультации'), ('Менеджмент'), ('Мобильные приложения');
"""