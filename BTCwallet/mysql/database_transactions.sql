use db;

CREATE TABLE transactions(
    transactionID INT not null AUTO_INCREMENT,
    amount FLOAT NOT NULL,
    spent BOOLEAN NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transactionID)
);

INSERT INTO transactions (amount, spent) VALUES
(1.0, FALSE);