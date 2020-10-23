DROP TABLE if exists Category;
DROP TABLE if exists Location;
DROP TABLE if exists User;
DROP TABLE if exists Item;
DROP TABLE if exists Includes;
DROP TABLE if exists Bid;

CREATE TABLE Category
(
 category_id   INT          NOT NULL UNIQUE,
 category_name VARCHAR(255) NOT NULL UNIQUE,
 PRIMARY KEY (category_id)
);
 
CREATE TABLE Location
(
 location_id INT          NOT NULL UNIQUE,
 location    VARCHAR(255) NOT NULL UNIQUE,
 country     VARCHAR(255),
 PRIMARY KEY (location_id)
);
CREATE TABLE User
(
 user_id     VARCHAR(255) NOT NULL UNIQUE,
 rating      INT          NOT NULL,
 location_id INT,
 PRIMARY KEY (user_id),
 FOREIGN KEY (location_id) REFERENCES Location (location_id)
);
 
CREATE TABLE Item
(
 item_id        INT          NOT NULL UNIQUE,
 name           VARCHAR(255) NOT NULL,
 currently      DOUBLE,
 buy_price      DOUBLE,
 first_bid      DOUBLE,
 number_of_bids INT          NOT NULL,
 started        datetime     NOT NULL,
 ends           datetime     NOT NULL,
 seller_id      VARCHAR(255) NOT NULL,
 description    VARCHAR(255) NOT NULL,
 PRIMARY KEY (item_id),
 FOREIGN KEY (seller_id) REFERENCES User (user_id)
);
 
CREATE TABLE Includes
(
 item_id     INT NOT NULL,
 category_id INT NOT NULL,
 PRIMARY KEY (item_id, category_id),
 FOREIGN KEY (item_id) REFERENCES Item (item_id),
 FOREIGN KEY (category_id) REFERENCES Category (category_id)
);


CREATE TABLE Bid
(
 bid_id    INT      NOT NULL UNIQUE,
 bidder_id VARCHAR(255)      NOT NULL,
 bid_item  INT      NOT NULL,
 bid_time  datetime NOT NULL,
 amount    DOUBLE   NOT NULL,
 PRIMARY KEY (bid_id),
 FOREIGN KEY (bidder_id) REFERENCES USER (user_id),
 FOREIGN KEY (bid_item) REFERENCES Item(item_id)
);
 