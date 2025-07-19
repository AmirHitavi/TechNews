# TechNews

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-FF9500?style=for-the-badge&logo=scrapy&logoColor=white)

This repository is for internship project.

## Requirements
- Python
- Django
- Django REST Framework
- Django Filter
- Scrapy
- Scrapy Playwright


## Challenge 1: REST API Implementation

### Features
- Database model for news articles with title, content, tags, and source
- API endpoint to CRUD for news and tags
- Filter news by tags
- Filter news by one or more keywords provided by user
- Filter news by excluding specific keywords from content
- Combine both inclusion and exclusion filters
- Unit tests for all functionality
  
### API Endpoints
- `GET /api/news/`: List all news articles with filtering capabilities
- `POST /api/news/`: Create new instance of news articles
- `GET /api/news/{id}/`: Get the details of news article
- `PUT /api/news/{id}/`: Update the details of news article
- `DELETE /api/news/`: Delete the news article

- `GET /api/tag/`: List all tags
- `POST /api/tag/`: Create new instance of tags
- `GET /api/tag/{id}/`: Get the details of tag item
- `PUT /api/tag/{id}/`: Update the details of tag item
- `DELETE /tag/news/`: Delete the tag item


### How to Run
1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements/local.txt
   ```
4. Run migrations:
   ```
   make migrate
   ```
5. Create a superuser (optional for admin access):
   ```
   make make-super
   ```
6. Run the development server:
   ```
   make runserver
   ```


### Running Tests
```
make test
or
make cov
```

## Challenge 2: News Data Collection

### Features
- Scraper for Zoomit website news
- Collects news with title, content, tags, and source
- Returns data in the same format as Challenge 1 API expects
- Can be integrated with the API database

### How to Run
1. Install Scrapy:
   ```
   pip install scrapy
   pip install scrapy-playwright
   playwright install
   ```
2. Run to scrape all the articles:
   ```
   python core/manage.py scrape_zoomit
   or
   make zoomit
   ```
3. Run to scrape just one single article:
   ```
   python core/manage.py scrape_single {url}
   ```

