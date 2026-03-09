"""
Script to create the PostgreSQL database
Run this before seed_data.py
"""

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file")
    exit(1)

# Parse the database URL
# Format: postgresql://username:password@host:port/database
parts = DATABASE_URL.replace("postgresql://", "").split("/")
db_name = parts[-1]
connection_string = f"postgresql://{'/'.join(parts[:-1])}"

print(f"🔧 Creating database: {db_name}")
print(f"📍 Connection: {connection_string}")

try:
    # Connect to default 'postgres' database to create our database
    engine = create_engine(connection_string + "/postgres")
    
    with engine.connect() as connection:
        # Check if database already exists
        result = connection.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        )
        
        if result.fetchone():
            print(f"✅ Database '{db_name}' already exists")
        else:
            # Create the database
            connection.execute(text(f"CREATE DATABASE {db_name}"))
            connection.commit()
            print(f"✅ Database '{db_name}' created successfully")
            
except Exception as e:
    print(f"❌ Error creating database: {str(e)}")
    exit(1)

print("\n✨ Database setup completed!")
print("Next step: Run 'python seed_data.py' to populate with dummy data")
