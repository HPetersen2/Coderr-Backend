import random

# Testdaten für Usernamen und andere Felder
usernames_customer = [f"customer_user_{i}" for i in range(10)]
usernames_business = [f"business_user_{i}" for i in range(10)]
domains = ["example.com", "devmail.com", "test.org"]
locations = ["Berlin", "Hamburg", "Munich", "Cologne", "Stuttgart"]
descriptions = [
    "Experienced backend developer with a focus on Django and Flask.",
    "Frontend wizard using React and Vue.",
    "Full-stack developer for modern web apps.",
    "Automation and CI/CD specialist.",
    "DevOps engineer with cloud expertise (AWS, GCP).",
    "UI/UX Designer with Figma and Adobe XD skills.",
    "Database administrator with PostgreSQL and MySQL experience.",
    "API integration specialist with REST and GraphQL knowledge.",
    "Software tester with Selenium and PyTest skills.",
    "Project manager for agile software teams."
]
features_sample = [
    ["Responsive Design", "SEO Optimization"],
    ["Admin Panel", "User Authentication"],
    ["REST API", "JWT Auth", "Stripe Integration"],
    ["Docker Support", "Kubernetes Deployment"],
    ["CI/CD Pipeline", "GitHub Actions"],
]

def generate_email(username):
    return f"{username}@{random.choice(domains)}"

# ---- 1. User & UserProfile ----
users_data = [
    {"username": u, "email": generate_email(u), "type": "customer"} for u in usernames_customer
] + [
    {"username": u, "email": generate_email(u), "type": "business"} for u in usernames_business
]

# ---- 2. Profile ----
profiles_data = []
for idx, user in enumerate(users_data):
    profiles_data.append({
        "user": user["username"],
        "first_name": f"First{idx}",
        "last_name": f"Last{idx}",
        "location": random.choice(locations),
        "tel": f"+49 170 {random.randint(1000000, 9999999)}",
        "description": random.choice(descriptions),
        "working_hours": "Mon-Fri, 9am-5pm"
    })

# ---- 3. Offers & OfferDetails ----
offers_data = []
offer_details_data = []
for i, business_user in enumerate(usernames_business):
    for j in range(2):  # 2 Offers pro Business-User
        offer_title = f"{random.choice(['Build', 'Design', 'Develop'])} {random.choice(['Website', 'API', 'App'])}"
        offer_id = f"offer_{i*2 + j}"
        offers_data.append({
            "user": business_user,
            "title": offer_title,
            "description": f"{offer_title} using modern tech stack."
        })
        for offer_type in ["basic", "standard", "premium"]:
            offer_details_data.append({
                "offer": offer_id,
                "title": f"{offer_type.capitalize()} Package",
                "revisions": random.randint(1, 5),
                "delivery_time_in_days": random.randint(1, 14),
                "price": round(random.uniform(50, 500), 2),
                "features": random.choice(features_sample),
                "offer_type": offer_type
            })

# ---- 4. Orders ----
orders_data = []
for i in range(20):
    customer = random.choice(usernames_customer)
    business = random.choice(usernames_business)
    orders_data.append({
        "customer_user": customer,
        "business_user": business,
        "title": f"Order #{i+1} - {random.choice(['Web App', 'Landing Page', 'REST API'])}",
        "revisions": random.randint(0, 5),
        "delivery_time_in_days": random.randint(3, 14),
        "price": round(random.uniform(100, 1000), 2),
        "features": random.choice(features_sample),
        "status": random.choice(["in_progress", "completed"])
    })

# ---- 5. Reviews ----
reviews_data = []
for i in range(20):
    business = random.choice(usernames_business)
    reviewer = random.choice([u for u in usernames_customer if u != business])
    reviews_data.append({
        "business_user": business,
        "reviewer": reviewer,
        "rating": random.randint(1, 5),
        "description": f"Review {i+1}: {random.choice(['Great job!', 'Satisfactory.', 'Exceeded expectations.', 'Could be better.', 'Would hire again.'])}"
    })

# Beispielausgabe
print("Sample Users:", users_data[:2])
print("Sample Profiles:", profiles_data[:2])
print("Sample Offers:", offers_data[:2])
print("Sample OfferDetails:", offer_details_data[:2])
print("Sample Orders:", orders_data[:2])
print("Sample Reviews:", reviews_data[:2])
