import pandas as pd
import sqlite3

# 1️⃣ Read Excel file
excel_file = "X:\smart_hr_system.xlsx"# your excel file name
df = pd.read_excel(excel_file)

# 2️⃣ Connect to SQLite database (it will create if not exists)
conn = sqlite3.connect("mydatabase.db")

# 3️⃣ Save Excel data to SQLite table
# Table name: users (you can change it)
df.to_sql("users", conn, if_exists="replace", index=False)

print("Data successfully saved to SQLite database!")

# 4️⃣ Close connection
conn.close()