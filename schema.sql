-- status визначення

CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE UNIQUE INDEX idx_status_name_unique ON status(name);



-- tasks визначення

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- users визначення

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE UNIQUE INDEX idx_users_email ON users(email);