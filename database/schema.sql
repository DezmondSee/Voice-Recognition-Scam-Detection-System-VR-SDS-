-- Phase 1: Database Setup
CREATE DATABASE IF NOT EXISTS vrsds_enterprise;
USE vrsds_enterprise;

-- Phase 2: Create Tables (With every column your code asks for)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    is_active TINYINT(1) DEFAULT 1,
    security_question VARCHAR(255),
    security_answer VARCHAR(255),
    -- Dual-column fix so both 'timestamp' and 'created_at' work
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS call_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    caller_id VARCHAR(20),
    verdict ENUM('SCAM', 'SAFE') NOT NULL,
    confidence_score FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scam_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reported_number VARCHAR(20) NOT NULL,
    description TEXT,
    status ENUM('pending', 'verified', 'dismissed') DEFAULT 'pending',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scan_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    file_name VARCHAR(255) NOT NULL,
    scam_probability FLOAT NOT NULL,
    prediction VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Phase 3: Initial Data (Ensures no "Empty Set" or "Invalid" errors)
INSERT INTO users (username, password_hash, email, role, is_active) 
VALUES ('admin', 'admin123', 'admin@uum.edu.my', 'admin', 1)
ON DUPLICATE KEY UPDATE username=username;

-- Seed data for the Dashboard charts and metrics
INSERT INTO call_logs (user_id, caller_id, verdict, confidence_score) VALUES (1, '+60123456789', 'SCAM', 0.98);
INSERT INTO scam_reports (user_id, reported_number, description) VALUES (1, '+601122334455', 'Initial system report');