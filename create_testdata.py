import os
import django
import random
from faker import Faker
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth.models import User
from offers_app.models import Offer, OfferDetail
from auth_app.models import UserProfile
from orders_app.models import Order
from reviews_app.models import Review

fake = Faker()

# --- Create Users and Profiles ---
user_profiles = []

for _ in range(30):
    username = fake.user_name()
    user = User.objects.create_user(
        username=username,
        email=fake.email(),
        password='password123'
    )
    profile_type = random.choice(['customer', 'business'])
    profile = UserProfile.objects.create(
        user=user,
        type=profile_type,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        location=fake.city(),
        tel=fake.phone_number(),
        description=fake.sentence(nb_words=12),
        working_hours=f"{random.randint(8,10)}am-{random.randint(5,8)}pm"
    )
    user_profiles.append(profile)

# --- Create Offers and OfferDetails ---
offer_details_list = []

for profile in user_profiles:
    if profile.type == 'business':
        for _ in range(random.randint(1,3)):  # 1-3 offers per business
            offer = Offer.objects.create(
                user=profile.user,
                title=fake.bs().title(),
                description=fake.sentence(nb_words=15)
            )
            for offer_type in ['basic', 'standard', 'premium']:
                detail = OfferDetail.objects.create(
                    offer=offer,
                    title=f"{offer.title} - {offer_type.title()}",
                    revisions=random.randint(1,5),
                    delivery_time_in_days=random.randint(1,14),
                    price=Decimal(random.randint(50,500)),
                    features=[fake.word() for _ in range(3)],
                    offer_type=offer_type
                )
                offer_details_list.append(detail)

# --- Create Orders ---
for _ in range(30):
    customer = random.choice([p.user for p in user_profiles if p.type == 'customer'])
    offer_detail = random.choice(offer_details_list)
    order = Order.objects.create(
        customer_user=customer,
        business_user=offer_detail.offer.user,
        offer_detail=offer_detail,
        price=offer_detail.price,
        status=random.choice(['in_progress', 'completed', 'cancelled'])
    )

# --- Create Reviews ---
for _ in range(30):
    reviewer = random.choice([p.user for p in user_profiles if p.type == 'customer'])
    business = random.choice([p.user for p in user_profiles if p.type == 'business'])
    Review.objects.create(
        business_user=business,
        reviewer=reviewer,
        rating=random.randint(1,5),
        description=fake.sentence(nb_words=12)
    )

print("Testdaten erfolgreich erstellt!")
