# Documentation for Article Fetcher Project

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Project](#running-the-project)
6. [Tasks](#tasks)
7. [Database Models](#database-models)
8. [Logging](#logging)


## Overview
This project fetches articles from various RSS feeds, processes them to classify their categories using Natural Language Processing (NLP) techniques, and stores them in a MySQL database. It uses Celery for asynchronous processing of articles.

## Requirements
To run this project, ensure you have the following installed:
- Python 3.6 or higher
- MySQL Server
- Redis Server (for Celery)
- Virtual environment (optional but recommended)

### Python Libraries
Install the required Python libraries using pip:
```bash
pip install sqlalchemy feedparser python-dateutil nltk redis celery
```

## Installation
1. Clone the Repository: If you haven't already cloned your repository, do so using:
```bash
git clone https://github.com/username/your-repo-name.git
cd your-repo-name
```

2. Set Up a Virtual Environment (optional): Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Install the above mentioned libraries.

## Configuration
1. MySQL Database:

  - Ensure you have a MySQL database set up. You need to create a database named news_collector.
  - Update the MySQL credentials in the fetcher.py and tasks.py files, or enter them when prompted.
2. RSS Feeds: You can modify the RSS_FEEDS list in the fetcher.py file to include any additional RSS feeds from which you     
want to fetch articles.

3. NLTK Resources: Uncomment the NLTK download lines in tasks.py to download the necessary resources (tokenizer and stopwords).

## Running the Project
1. Start Redis Server: Ensure that your Redis server is running. You can start it using:
```bash
redis-server
```
2. Start Celery Worker: Open a new terminal, navigate to your project directory, and start the Celery worker:
 ```bash
 celery -A tasks worker --loglevel=info --pool=threads
3. Run the Fetcher Script: In another terminal, run the fetcher.py script:
 ```bash
 python fetcher.py
```
- Enter the database credential when prompted upon after running the fetcher.py

## Tasks
# Article Classification
Articles are classified based on keywords defined in the classify_article function in tasks.py. You can modify the keyword lists to adjust the classification categories.
# Logging
The project uses Python’s built-in logging library to log information about article fetching and processing. Logs will display in the terminal where you run the fetcher and Celery worker.

## Database Models
The project uses SQLAlchemy for database interaction. The Article model is defined in models.py with the following attributes:

- id: Primary key
- title: Title of the article
- publication_date: Date and time of publication
- source_url: Unique URL of the article
- category: Classified category of the article

