# 🎬 IMDb Movie Scraper with Django & REST API

This project is a Django-based web scraper that extracts movie information from IMDb using a keyword or genre (e.g., "comedy", "action"), stores the data in a SQLite database via Django ORM, and provides both a web interface and REST API to access the data.

---

## 🚀 Features

- 🔍 Search IMDb by genre or keyword
- 🌐 Scrape movie details:
  - Title
  - Release Year
  - IMDb Rating
  - Director(s)
  - Cast
  - Plot Summary
- 📄 Pagination through search results (IMDb)
- 🧠 Concurrent scraping for performance
- 💾 Store results in database using Django ORM
- 🧩 REST API to query stored movie data
- 🖥️ Web UI to trigger scraping and view results (with loading indicator)
- ✅ Unit test-ready
- 🛠️ Error handling and logging

---

## 📂 Project Structure

imdb-web-scraper/
├── web-scraper/ # Main Django project directory
│ ├── imdb_ratings/ # Main app for scraping and movie management
│ │ ├── migrations/
│ │ │ ├── init.py
│ │ │ └── 0001_initial.py
│ │ ├── templates/imdb_ratings/
│ │ │ ├── movie_list.html
│ │ │ └── scrape_form.html
│ │ ├── static/
│ │ │ ├── css/styles.css
│ │ │ └── js/scripts.js
│ │ ├── management/commands/
│ │ │ ├── init.py
│ │ │ └── clear_movies.py
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── models.py
│ │ ├── scraper.py
│ │ ├── serializer.py
│ │ ├── tests.py
│ │ ├── urls.py
│ │ ├── views.py
│ │ └── forms.py
│ ├── scraper_site/
│ │ ├── init.py
│ │ ├── asgi.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ │ └── admin.py
│ ├── db.sqlite3
│ └── manage.py
├── README.md
├── requirements.txt
└── project_details.txt

---

## 📦 Installation

### 1. Clone the repository

`git clone https://github.com/pmaletia/imdb-web-scraper.git`

### 2. Create a virtual environment
`python -m venv env`
`source env/bin/activate`   # On Windows: `env\Scripts\activate`

3. Install dependencies

`pip install -r app_requirements.txt`
`cd imdb-web-scraper/web-scraper`

4. Run migrations
`python manage.py makemigrations`
`python manage.py migrate`

5. Start the development server
`python manage.py runserver`


🧪 How to Use
▶️ Web Interface
Open your browser and go to: http://127.0.0.1:8000/api

Enter a keyword or genre (e.g., comedy, thriller) and hit Submit

Wait while the scraper runs (UI will show a loader)

🔌 API Endpoint
Method	URL	Description
GET	/api/scrape/	List all movies
GET	/api/movie-search/?q=comedy	Filter movies by keyword

Example:

curl http://127.0.0.1:8000/api/movie-search/?q=action
✅ Running Tests
python manage.py test


⚙️ Tech Stack
Python 3.x

Django

Django REST Framework

BeautifulSoup

Requests

concurrent.futures

Bootstrap (for UI)

SQLite (default DB)

Selenium

📌 Notes
IMDb doesn't provide a public API. This project scrapes IMDb search pages (respect robots.txt usage for production).

This is intended for educational and personal use only.

✨ Bonus Features Implemented
✅ Concurrent scraping using concurrent.futures.ThreadPoolExecutor

✅ UI loading animation until all poster images load

✅ Optional keyword/genre parameter via POST

✅ Basic error handling and logging

👩‍💻 Author
Developed with ❤️ by Priyanka Maletia

