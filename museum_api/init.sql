-- Initialize database with proper character set and collation
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Create database if not exists (this is usually handled by MYSQL_DATABASE env var)
-- CREATE DATABASE IF NOT EXISTS museum_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE museum_bot;

-- Grant privileges to the application user
GRANT ALL PRIVILEGES ON museum_bot.* TO 'museum_user'@'%';
FLUSH PRIVILEGES;

SET FOREIGN_KEY_CHECKS = 1; 