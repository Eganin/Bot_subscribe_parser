
CREATE TABLE subscriptions(
    id INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    user_id VARCHAR (255) NOT NULL
                          UNIQUE ,
    status BOOLEAN  NOT NULL DEFAULT (TRUE)
);