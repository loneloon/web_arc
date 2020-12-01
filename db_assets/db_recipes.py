# The following are sql scripts for certain tables used by db

COMMENTS = "CREATE TABLE IF NOT EXISTS messages "\
            "(id INTEGER PRIMARY KEY AUTOINCREMENT,"\
            "name VARCHAR(16) DEFAULT 'anonymous',"\
            "email VARCHAR(16),"\
            "subject VARCHAR(16) DEFAULT 'empty',"\
            "text VARCHAR(25) DEFAULT 'empty');"

USERS = "CREATE TABLE IF NOT EXISTS users "\
            "(id INTEGER PRIMARY KEY AUTOINCREMENT,"\
            "login VARCHAR(16) UNIQUE,"\
            "password VARCHAR(32),"\
            "first_name VARCHAR(16),"\
            "last_name VARCHAR(16),"\
            "email VARCHAR(16),"\
