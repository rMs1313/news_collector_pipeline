from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database Configuration
username = input("Enter Username of MySQL Database: ")
password = input("Enter Password: ")
host = input("Enter Hostname: ")  
port = input("Enter Port No: ")    
database_name = 'news_collector'

# Construct the Database URI
DATABASE_URI = f'mysql://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

