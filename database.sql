DROP TABLE IF EXISTS urls;
CREATE TABLE IF NOT EXISTS urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE NOT NULL
);

DROP TABLE IF EXISTS url_checks;
CREATE TABLE IF NOT EXISTS url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT NOT NULL,
    status_code BIGINT,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at DATE NOT NULL
);
