CREATE DATABASE IF NOT EXISTS vrsds_enterprise;
USE vrsds_enterprise;

-- 1. Create the Users table WITH the new columns!
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255),                  -- NEW
    security_question VARCHAR(255),      -- NEW
    security_answer VARCHAR(255),        -- NEW
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Scan History table
CREATE TABLE IF NOT EXISTS scan_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    scan_type ENUM('text', 'audio') NOT NULL,
    content TEXT NOT NULL,
    prediction_result VARCHAR(50) NOT NULL,
    confidence_score FLOAT DEFAULT 0.0,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Create the Model Training Logs table
CREATE TABLE IF NOT EXISTS model_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_type ENUM('text', 'audio') NOT NULL,
    accuracy_score FLOAT NOT NULL,
    dataset_name VARCHAR(255) NOT NULL,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Insert the Default Admin Account (updated with dummy data for the new columns)
INSERT IGNORE INTO users (username, password_hash, email, security_question, security_answer, role) 
VALUES ('admin', 'admin123', 'admin@vrsds.com', 'admin_q', 'admin_a', 'admin');