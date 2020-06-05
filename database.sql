
CREATE TABLE subscriptions_stopgame(
    id INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    user_id VARCHAR (255) NOT NULL
                          UNIQUE ,
    status BOOLEAN  NOT NULL DEFAULT (TRUE)
);

CREATE TABLE subscriptions_crackwatch(
    id INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    user_id VARCHAR (255) NOT NULL
                          UNIQUE ,
    status BOOLEAN  NOT NULL DEFAULT (TRUE)
);

CREATE TABLE subscriptions_habr(
    id INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    user_id VARCHAR (255) NOT NULL
                          UNIQUE ,
    status BOOLEAN  NOT NULL DEFAULT (TRUE)

);