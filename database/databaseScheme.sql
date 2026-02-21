CREATE DATABASE IF NOT EXISTS vrsds_enterprise;
USE vrsds_enterprise;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    security_question VARCHAR(255),
    security_answer VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS call_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    scan_type VARCHAR(10),
    verdict VARCHAR(20),
    confidence FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE IF NOT EXISTS trusted_contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    contact_name VARCHAR(50),
    phone_number VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS scam_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    phone_number VARCHAR(20),
    category VARCHAR(50),
    description TEXT,
    status ENUM('PENDING', 'REVIEWED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Default Admin Account
INSERT IGNORE INTO users (username, password_hash, email, security_question, security_answer, role) 
VALUES ('admin', 'admin123', 'admin@vrsds.com', 'What is your role?', 'admin', 'admin');