# TechNews

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-FF9500?style=for-the-badge&logo=scrapy&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

This repository is for internship project.

## Requirements
- Python
- Django
- Django REST Framework
- Django Filter
- Scrapy
- Scrapy Playwright
- Celery
- Redis
- Docker

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


## Challenge 2: News Data Collection

### Features
- Scraper for Zoomit website news
- Collects news with title, content, tags, and source
- Returns data in the same format as Challenge 1 API expects
- Can be integrated with the API database


## Challenge 3: Celery & Dockerization

### Features
- Added Celery for periodic news scraping tasks
- Configured Celery Beat for scheduling
- Redis as message broker
- Flower for monitoring Celery tasks
- Dockerized the entire application

### New Components
- Redis container (message broker)
- Celery worker container
- Celery beat container
- Flower container (monitoring)


## How to Run
1. Build and start containers:
   ```
   docker-compose up -d --build
   ```
2. Access services:
   - Django app: http://localhost:8000
   - Flower (Celery monitoring): http://localhost:5555
   - Pgadmin: http://localhost:5050
3. To stop:
   ```
   docker-compose down
   ```
4. To test:
   ```
   make pytest
   or 
   make pytest-cov
   ```
5. Run to scrape all the articles:
   ```
   docker exec -it api python core/manage.py scrape_zoomit
   or
   make zoomit
   ```
6. Run to scrape just one single article:
   ```
   docker exec -it api python core/manage.py scrape_single {url}

   ```

### Environment Variables
Configure in `.env` file:
```
LOCAL_SECRET_KEY=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
DATABASE_URL=

PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

CELERY_FLOWER_USER=
CELERY_FLOWER_PASSWORD=
```