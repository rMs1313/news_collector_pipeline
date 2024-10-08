# fetcher.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dateutil import parser
import feedparser
from models import Article
from tasks import process_article

#username = root
#password = 1313
#localhost
#Port = 3305

username = input("Enter Username of MySQL Database: ")
password = input("Enter Password: ")
host = input("Enter Hostname: ")  
port = input("Enter Port No: ")    
database_name = 'news_collector'

# Construct the Database URI
DATABASE_URI = f'mysql://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://qz.com/feed",
    "http://feeds.reuters.com/reuters/businessNews",
    'http://feeds.feedburner.com/NewshourWorld',
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
]

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful:", result.fetchone())
    except Exception as e:
        print("Connection failed:", e)

def fetch_articles():
    session = Session()
    try:
        for feed in RSS_FEEDS:
            try:
                parsed_feed = feedparser.parse(feed)
                for entry in parsed_feed.entries:
                    if hasattr(entry, 'title') and hasattr(entry, 'link') and hasattr(entry, 'published'):
                        title = entry.title
                        source_url = entry.link
                        publication_date_str = entry.published

                        try:
                            publication_date = parser.parse(publication_date_str)
                            formatted_date = publication_date.strftime('%Y-%m-%d %H:%M:%S')  # Change to full date-time format
                        except ValueError:
                            print(f"Invalid date format for entry: {publication_date_str}")
                            continue

                        # Check if the article already exists
                        if not session.query(Article).filter_by(source_url=source_url).first():
                            new_article = Article(
                                title=title,
                                publication_date=formatted_date,
                                source_url=source_url,
                                category=None  # Initialize category as None
                            )
                            session.add(new_article)
                            session.commit()  # Commit to save new article
                            
                            # Process article to classify it
                            process_article.delay(new_article.id)  # Send article to Celery for processing

            except Exception as e:
                print(f"Error fetching articles from {feed}: {e}")
                session.rollback()

    except Exception as e:
        print(f"Error during article fetching: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    test_connection()
    fetch_articles()
