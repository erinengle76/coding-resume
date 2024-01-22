CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(200) PRIMARY KEY,
    password_hash VARCHAR(200),
    email VARCHAR(200),
    verified INTEGER
);

CREATE TABLE IF NOT EXISTS finance_relations (
    id SERIAL PRIMARY KEY,
    username VARCHAR(200),
    symbol VARCHAR(200)
);
