DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS models CASCADE;
DROP TABLE IF EXISTS brands CASCADE;

CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) UNIQUE
);

CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    brand_id INTEGER,
    model_name VARCHAR(255),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    model_id INTEGER,
    year INTEGER,
    price INTEGER,
    title VARCHAR(255),
    link VARCHAR(500),
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);