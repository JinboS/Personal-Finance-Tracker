import sqlite3

# 连接到 finance.db（如果文件不存在，会自动创建）
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# 创建记录表（与之前 Flask 代码中使用的表结构一致）
cursor.execute("""
CREATE TABLE IF NOT EXISTS record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,  -- 'income' 或 'expense'
    description TEXT,
    amount REAL NOT NULL
)
""")

# 插入一些示例数据
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

print("finance.db 已生成并插入测试数据。")
