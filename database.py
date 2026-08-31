import os
import psycopg2
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

DATABASE_URL = "postgresql://finance_tracker_tkxs_user:tP5om78VyKvw1EqKoLJGtzGtAoSzXxut@dpg-da1pdk2jnfac739v7q4g-a.oregon-postgres.render.com/finance_tracker_tkxs" #os.getenv("DATABASE_URL")

def get_connection():
    
    """Establish a connection to the PostgreSQL database."""
    
    if not DATABASE_URL:
        print("DATABASE_URL is not set in the environment variables.")
        return None
    
    try:
        print(f"Connecting to the database...")
        
        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode='require', 
            connect_timeout=10)
        
        print("Database connection established successfully.")
        return conn
    
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
    
def create_tables():
    
    """Create the necessary tables for the finance tracker app."""
    
    conn = get_connection()
    
    if conn is None:
        print("Failed to connect to the database. Tables not created.")
        return

    try:
        with conn.cursor() as cursor:
            
            # ---------------------
            # USERS
            # ---------------------
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # ---------------------
            # ACCOUNTS
            # ---------------------
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    account_name VARCHAR(100) NOT NULL,
                    account_type VARCHAR(50) NOT NULL,
                    current_balance NUMERIC(12, 2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE
                );
            """)
            
            # ---------------------
            # CATEGORIE
            # ---------------------
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    category_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    category_name VARCHAR(100) NOT NULL,
                    category_type VARCHAR(50) NOT NULL,
                    
                    CHECK (category_type IN ('income', 'expense')),
                    
                    FOREIGN KEY (user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE
                );
            """)
            
            # ---------------------
            # TRANSACTIONS
            # ---------------------
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    account_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    amount NUMERIC(12, 2) NOT NULL,
                    transaction_type VARCHAR(50) NOT NULL,
                    description TEXT,
                    transaction_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    CHECK (transaction_type IN ('income', 'expense')),  
                    CHECK (amount > 0),
                    
                    FOREIGN KEY (user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE,
                    
                    FOREIGN KEY (account_id)
                        REFERENCES accounts(account_id)
                        ON DELETE CASCADE,
                        
                    FOREIGN KEY (category_id)
                        REFERENCES categories(category_id)
                        ON DELETE RESTRICT
                );
            """)
            
            # ---------------------
            # BUDGETS
            # ---------------------
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    budget_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    monthly_limit NUMERIC(12, 2) NOT NULL,
                    budget_month DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    CHECK (monthly_limit > 0),

                    FOREIGN KEY (user_id)
                        REFERENCES users(user_id)
                        ON DELETE CASCADE,

                    FOREIGN KEY (category_id)
                        REFERENCES categories(category_id)
                        ON DELETE RESTRICT,
                        
                    UNIQUE (user_id, category_id, budget_month)
                );
            """)
            
            conn.commit()
            print("Tables created successfully.")
            
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
        
    finally:
        if cursor is not None:
            cursor.close()
        
        if conn is not None:
            conn.close()
            print("Database connection closed.")