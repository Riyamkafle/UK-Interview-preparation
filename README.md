<<<<<<< HEAD
# UK-Interview-preparation
=======
# UK University Interview Prep API

Production-ready Django REST API for UK university interview preparation.
Supports 31 universities popular among Nepali students.

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Seed data (universities + questions)
python manage.py seed_data

# 4. (Optional) Create admin user
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

API is now live at: http://127.0.0.1:8000/api/

---

## 🏫 Universities (31 total)

### Original 25
University of Greenwich, University of East London, Middlesex University,
Coventry University, University of Hertfordshire, University of West London,
Birmingham City University, University of Sunderland, University of Essex,
University of Leicester, University of Westminster, Northumbria University,
De Montfort University, University of Bedfordshire, University of Roehampton,
University of South Wales, Teesside University, Anglia Ruskin University,
University of Gloucestershire, University of Northampton, University of Bradford,
University of Derby, Sheffield Hallam University, Liverpool John Moores University,
University of Portsmouth

### Added 6
BPP University, Ravensbourne University London, University of East London (updated),
University of West London (updated), University of Roehampton (updated),
Ulster University

---

## 🔌 API Endpoints

### 1. List / Search Universities
```
GET /api/universities/
GET /api/universities/?search=bpp
```

Response:
```json
{
  "count": 31,
  "results": [
    { "id": 1, "name": "BPP University", "country": "UK", "has_custom_questions": true }
  ]
}
```

---

### 2. Get Questions for a University
```
GET /api/questions/?university_id=1
```

- If `has_custom_questions = true` → returns common + custom questions
- Otherwise → returns only common questions

---

### 3. Evaluate Answers
```
POST /api/evaluate/
Content-Type: application/json

{
  "answers": [
    { "question_id": 1, "answer": "I chose this course because..." },
    { "question_id": 3, "answer": "I want to study in the UK because..." }
  ]
}
```

Response:
```json
{
  "overall_score": 72,
  "status": "moderate",
  "color": "yellow",
  "final_message": "You're close — improve the flagged areas and you'll do well.",
  "feedback": [
    {
      "question": "Why did you choose this course?",
      "score": 80,
      "issues": [],
      "suggestions": []
    }
  ],
  "improvement_topics": ["financial explanation"]
}
```

---

## 📊 Score Logic

| Score | Status   | Color  |
|-------|----------|--------|
| > 75  | strong   | green  |
| 50–75 | moderate | yellow |
| < 50  | weak     | red    |

Each answer scored on 5 criteria (+20 each):
- Length > 50 chars
- Career keywords mentioned
- UK justification present
- Financial planning mentioned
- Structured (2+ sentences)

---

## 🛠 Admin Panel

Visit: http://127.0.0.1:8000/admin/

Manage universities and questions directly from the admin UI.

---

## 🚀 Deployment (Railway / VPS)

```bash
# Set environment variable in production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Use gunicorn
gunicorn interview_prep.wsgi:application --bind 0.0.0.0:8000
```

For PostgreSQL, update `DATABASES` in `settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}
```

---

## 🔄 Reseed Data

```bash
python manage.py seed_data --clear
```
>>>>>>> 6b9ff63 (Initial commit)
