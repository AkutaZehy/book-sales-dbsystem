-- 创建图书表
CREATE TABLE Book (
    isbn VARCHAR(13) PRIMARY KEY NOT NULL,
    title VARCHAR(100),
    price DECIMAL(10, 2) CHECK (price >= 0),
    author VARCHAR(100),
    category_id VARCHAR(50),
    publisher_id VARCHAR(50),
    publish_date DATE,
    FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

-- 创建类别表
CREATE TABLE Category (
    category_id VARCHAR(50) PRIMARY KEY NOT NULL,
    category_name VARCHAR(100),
    description TEXT
);

-- 创建出版社表
CREATE TABLE Publisher (
    publisher_id VARCHAR(50) PRIMARY KEY NOT NULL,
    publisher_name VARCHAR(100),
    contact_person VARCHAR(100),
    phone_number VARCHAR(20)
);

-- 创建客户表
CREATE TABLE Customer (
    customer_id VARCHAR(50) PRIMARY KEY NOT NULL,
    customer_name VARCHAR(100),
    password VARCHAR(100),
    register_date DATE,
    login_count INTEGER CHECK (login_count >= 0),
    account_balance DECIMAL(10, 2) CHECK (account_balance >= 0)
);

-- 创建订单表
-- 注意 Order 是保留字！
CREATE TABLE Orders (
    order_id VARCHAR(50) PRIMARY KEY NOT NULL,
    customer_id VARCHAR(50),
    order_date DATE,
    total_amount DECIMAL(10, 2) CHECK (total_amount >= 0),
    payment_status VARCHAR(50) CHECK (payment_status IN ('未支付', '已支付')),
    logistics_status VARCHAR(50) CHECK (logistics_status IN ('未发货', '已发货未完成', '已完成', '订单异常')),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- 创建订单明细表
CREATE TABLE OrderDetail (
    order_detail_id VARCHAR(50) PRIMARY KEY NOT NULL,
    order_id VARCHAR(50),
    isbn VARCHAR(13),
    unit_price DECIMAL(10, 2) CHECK (unit_price > 0),
    quantity INTEGER CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (isbn) REFERENCES Book(isbn)
);
