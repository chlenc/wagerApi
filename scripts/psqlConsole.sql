DROP TABLE users;

CREATE TABLE users
(
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(255) NOT NULL,
    password    VARCHAR(255),
    seed        VARCHAR(255),
    salt        VARCHAR(255),
    status      VARCHAR(255),
    pendingHash VARCHAR(32)
);

INSERT INTO users (username, password, seed, salt, status)
VALUES ('admin', '1', 'test test test', '', 'registered');

INSERT INTO users (username, status, pendingHash)
VALUES ('user1', 'pending', 'osuuymgwyebldxdidlmwqhhxchtbxgbq');

