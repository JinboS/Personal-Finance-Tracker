import sqlite3

# # Connect to finance.db (if the file does not exist, it will be automatically created)
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# Create the record table (consistent with the table structure used in the previous Flask code)
cursor.execute("""
CREATE TABLE IF NOT EXISTS record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,  -- 'income' 或 'expense'
    description TEXT,
    amount REAL NOT NULL
)
""")

# Insert some sample data
sample_data = [
    ("2023-01-01", "income", "Salary", 5000),
    ("2023-01-05", "expense", "Groceries", 150),
    ("2023-01-10", "expense", "Rent", 1200),
    ("2023-01-15", "income", "Freelance", 800),
    ("2023-01-20", "expense", "Utilities", 100)
]

cursor.executemany("""
INSERT INTO record (date, category, description, amount)
VALUES (?, ?, ?, ?)
""", sample_data) 

conn.commit()
conn.close()

print("finance.db Test data has been generated and inserted.")
