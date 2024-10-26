DROP TABLE IF EXISTS roles;
CREATE TABLE roles(
id INTEGER PRIMARY KEY autoincrement,
name VARCHAR(16)
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations(
id INTEGER PRIMARY KEY autoincrement,
country VARCHAR(56),
city VARCHAR(120)
);

DROP TABLE IF EXISTS file_types;
CREATE TABLE file_types(
id INTEGER PRIMARY KEY autoincrement,
type VARCHAR(16)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users(
id INTEGER PRIMARY KEY autoincrement,
fullname VARCHAR(120),
phone INTEGER,
email VARCHAR(120),
created_at DATE,
updated_at DATE,
role_id INTEGER,
location_id INTEGER,
FOREIGN KEY (role_id) REFERENCES roles (id),
FOREIGN KEY (location_id) REFERENCES locations (id)
);

DROP TABLE IF EXISTS files;
CREATE TABLE files(
id INTEGER PRIMARY KEY autoincrement,
link VARCHAR(256),
created_at DATE,
user_id INTEGER,
type_id INTEGER,
FOREIGN KEY (user_id) REFERENCES users (id),
FOREIGN KEY (type_id) REFERENCES file_types (id)
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts(
id INTEGER PRIMARY KEY autoincrement,
text TEXT,
created_at DATE,
is_publish BOOLEAN,
user_id INTEGER,
FOREIGN KEY (user_id) REFERENCES users (id)
);

DROP TABLE IF EXISTS files_posts;
CREATE TABLE files_posts(
id INTEGER PRIMARY KEY autoincrement,
file_id INTEGER,
post_id INTEGER,
FOREIGN KEY (file_id) REFERENCES files (id),
FOREIGN KEY (post_id) REFERENCES posts (id)
);

