from sqlalchemy import create_engine, text

# Adjust the path to your database file
engine = create_engine("sqlite:///C:/Git Repos/new_hawaii.sqlite")

# Use a raw SQL query with the 'text' module
with engine.connect() as connection:
    result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = [row[0] for row in result]
    print("Tables in the database:", tables)