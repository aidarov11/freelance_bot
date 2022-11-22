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

create table adverts (
id serial primary key,
title text,
description text,
category_id int,
deadline text,
price text,
contacts text,
is_verified boolean default false,
user_id int,
created_at timestamp default current_timestamp,
is_hidden boolean default false
);

create table categories (
id serial primary key,
name text
);

insert into categories (name) values ('Дизайн и Арт'), ('Тексты'), ('Программирование'), ('Аудио/Видео'), ('Разработка игр'), ('Реклама и Маркетинг'), ('Аутсорсинг и консалтинг'), ('Анимация и флеш'), ('3D Графика'), ('Фотография'), ('Инжиниринг'), ('Архитектура/Интерьер'), ('Оптимизация (SEO)'), ('Полиграфия'), ('Обучение и консультации'), ('Менеджмент'), ('Мобильные приложения');
