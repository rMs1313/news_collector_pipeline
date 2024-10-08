import logging
import nltk
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from models import Article

porter_stemmer = PorterStemmer()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download necessary NLTK resources (only do this once, or you can comment it out later)
#nltk.download('punkt')  # Download tokenizer
#nltk.download('stopwords')  # Download stopwords for filtering

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Celery Configuration
app = Celery('tasks', broker='redis://localhost:6379/0')  # Assuming you use Redis as the broker

# Database Configuration
username = 'root'
password = '1313'
host = 'localhost'
port = '3305'
database_name = 'news_collector'
DATABASE_URI = f'mysql://{username}:{password}@{host}:{port}/{database_name}'

# Create database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Load English stopwords
stop_words = set(stopwords.words('english'))

# Category classification function using NLTK
def classify_article(article_title):
    # Tokenize the title and filter out stopwords
    tokens = word_tokenize(article_title.lower())
    filtered_tokens = [porter_stemmer.stem(word) for word in tokens if word.isalnum() and word not in stop_words]
    # Define keywords for each category
    categories = {
        "Terrorism": ['terrorism', 'bomb', 'attack', 'violence','shooting','dead','dies','attacked'],
        "Crime": ['criminal','police','suspect','guns','murder'],
        "Protest": ['protest', 'demonstration', 'rally', 'march'],
        "Political Unrest": ['unrest', 'revolt', 'disturbance', 'chaos','war','protest','arrests','nuclear'],
        "Riot": ['riot', 'rioting', 'uprising', 'civil disturbance','standoff'],
        "Positive": ['positive', 'uplifting', 'hope', 'success','happy'],
        "Natural Disasters": ['earthquake', 'flood', 'hurricane', 'tornado','lanslide','heavy rain'],
        "Politics": ['politics', 'government', 'election', 'policy','vote','minister'],
        "Technology": ['technology', 'tech', 'innovation', 'gadget'],
        "Health": ['health','doctors','doctor','eating','foods', 'medicine', 'disease', 'virus']
    }
    stemmed_categories = {category: [porter_stemmer.stem(keyword) for keyword in keywords] for category, keywords in categories.items()}

    # Check for each category based on keywords
    for category, keywords in stemmed_categories.items():
        if any(porter_stemmer.stem(word) in keywords for word in filtered_tokens):
            return category

    return "Others"

@app.task
def process_article(article_id):
    session = Session()
    try:
        article = session.query(Article).get(article_id)
        if article:
            category = classify_article(article.title)
            article.category = category
            session.commit()
            logger.info(f"Article ID {article_id} classified as {category}.")
    except Exception as e:
        logger.error(f"Error processing article ID {article_id}: {e}")
        session.rollback()
    finally:
        session.close()

