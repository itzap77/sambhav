DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, email TEXT UNIQUE, role TEXT
);

CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT
);

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    category_id INTEGER, name TEXT, price REAL, stock_qty INTEGER, image_url TEXT,
    FOREIGN KEY(category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    total_amt REAL, status TEXT DEFAULT 'Confirmed'
);

CREATE TABLE Order_Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    order_id INTEGER, product_id INTEGER, qty INTEGER, price_locked REAL,
    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);

INSERT INTO Categories (name) VALUES ('Electronics'), ('Apparel'), ('Accessories');
INSERT INTO Products (category_id, name, price, stock_qty, image_url) VALUES 
(1, 'Gaming Laptop', 85000.00, 5, 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&q=80'),
(1, 'Mechanical Keyboard', 4500.00, 15, 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=500&q=80'),
(2, 'Sambhavs Store Hoodie', 1200.00, 50, 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&q=80'),
(1, 'HP 15s Core i3 Laptop', 38000.00, 10, 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&q=80'),
(1, 'KZ Castor Pro IEMs', 1800.00, 25, 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=500&q=80'),
(1, 'Audiocular Note Portable DAC', 3500.00, 20, 'https://images.unsplash.com/photo-1615592389070-bcc97e0504d3?w=500&q=80'),
(2, 'Ultra-Wide Fit Running Shoes', 2500.00, 30, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80'),
(3, 'Heavy Duty Hand Gripper', 450.00, 50, 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&q=80'),
(3, 'Blox Fruits Kitsune Plush', 900.00, 100, 'https://images.unsplash.com/photo-1558244402-286dd748c593?w=500&q=80');
