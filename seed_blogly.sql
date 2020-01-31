-- from the terminal run:
-- psql < seed_blogly.sql

DROP DATABASE IF EXISTS  blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    img_url Text NOT NULL default='https://images.unsplash.com/photo-1580329503754-35ddb65d49a8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'
)

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
)

);