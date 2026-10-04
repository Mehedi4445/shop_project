# Shop Product API

Django + Django REST Framework API. Anyone can list products; only authenticated users (token) can add them.

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

## Create a test user and token
```bash
python manage.py createsuperuser          # or create any user via the shell
python manage.py drf_create_token <username>
```
Copy the printed token.

## Run
```bash
python manage.py runserver
```

## Endpoints
| Method | URL | Auth |
|---|---|---|
| GET | `/api/products/` (`?page=2`) | none |
| POST | `/api/products/` | `Authorization: Token YOUR_TOKEN` |

Page size is 5. Products are ordered by id.

POST body (Postman: Body -> raw -> JSON):
```json
{"name": "Notebook", "description": "A notebook with 100 pages.", "price": "120.00", "stock": 25}
```

Validation: name not empty, price > 0, stock a whole number >= 0.
Missing/invalid token on POST returns 401.

## Tests
```bash
python manage.py test
```

## Screenshots
Add to `screenshots/`: product list, product created, auth error (401), validation error (400), page two.
