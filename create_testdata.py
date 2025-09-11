import requests
from faker import Faker

fake = Faker("de_DE")

BASE_URL = "http://127.0.0.1:8000"  # Passe bei Bedarf an

NUM_USERS = 30
NUM_OFFERS = 15

# Basic Offer Details Template
def get_offer_details(title):
    return [
        {
            "title": f"Basic {title}",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 150,
            "features": ["Code Review", "Bugfixing"],
            "offer_type": "basic"
        },
        {
            "title": f"Standard {title}",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 300,
            "features": ["Code Review", "Bugfixing", "Unit Tests"],
            "offer_type": "standard"
        },
        {
            "title": f"Premium {title}",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 600,
            "features": ["Code Review", "Bugfixing", "Unit Tests", "Refactoring"],
            "offer_type": "premium"
        }
    ]

offer_titles = [
    "Webentwicklung mit React",
    "Backend mit Node.js",
    "REST API mit Django",
    "Fullstack App mit Laravel",
    "Mobile App mit Flutter",
    "Scraping-Service mit Python",
    "Shopify Store Entwicklung",
    "WooCommerce Custom Plugin",
    "WordPress Website",
    "KI-Integration in Webanwendung",
    "DevOps Setup mit Docker",
    "CI/CD-Pipeline mit GitHub Actions",
    "Code Review für Java-Projekte",
    "Individuelles PHP-Modul",
    "Performance Optimierung"
]

registered_users = []

# Registrierung
for i in range(NUM_USERS):
    user_type = "business" if i < NUM_OFFERS else "customer"
    user_data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "test1234",
        "repeated_password": "test1234",
        "type": user_type
    }

    response = requests.post(f"{BASE_URL}/api/registration/", json=user_data)
    
    if response.status_code == 201:
        print(f"[✔] User erstellt: {user_data['username']} ({user_type})")
        registered_users.append({
            **user_data,
            "id": response.json().get("id"),  # falls zurückgegeben
        })
    else:
        print(f"[✘] Fehler bei User {user_data['username']}: {response.text}")

# Business-User einloggen & Angebote posten
for i, user in enumerate(registered_users[:NUM_OFFERS]):
    # Authentifiziere den User (angenommen, JWT oder Session nicht nötig)
    login_response = requests.post(f"{BASE_URL}/api/token/", data={
        "username": user["username"],
        "password": user["password"]
    })

    if login_response.status_code != 200:
        print(f"[✘] Login fehlgeschlagen für {user['username']}")
        continue

    token = login_response.json()["access"]
    headers = {"Authorization": f"Bearer {token}"}

    # Erstelle Angebot
    offer_title = offer_titles[i]
    offer_data = {
        "title": offer_title,
        "image": None,
        "description": fake.text(max_nb_chars=100),
        "details": get_offer_details(offer_title)
    }

    offer_response = requests.post(f"{BASE_URL}/api/offers/", json=offer_data, headers=headers)

    if offer_response.status_code == 201:
        print(f"[✔] Angebot erstellt für {user['username']}: {offer_title}")
    else:
        print(f"[✘] Fehler beim Angebot: {offer_response.text}")
