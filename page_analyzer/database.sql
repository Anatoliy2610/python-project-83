CREATE TABLE IF NOT EXISTS urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE
);

CREATE TABLE IF NOT EXISTS url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT,
    status_code BIGINT,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at DATE
);


CREATE TABLE IF NOT EXISTS test (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT,
    status_code BIGINT,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at DATE
);
drop table test;
drop table url_checks;
drop table urls;

INSERT INTO test (description) VALUES ('WWW');
INSERT INTO test (url_id, status_code, h1, title, description, created_at) VALUES (3, 400, 'qweqwe', 'asd', 'WWW');
INSERT INTO test (url_id, status_code, h1, title, description) VALUES (4, 200, 'asdasd', "asd", "SSS");
INSERT INTO test (url_id, status_code, h1, title, description) VALUES (5, 300, 'zxczxc', "asda", "XXX");
select * from test;

-- https://ru.hexlet.io
-- https://ya.ru
-- https://qna.habr.com
