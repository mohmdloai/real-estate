import io
import random

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from faker import Faker
from PIL import Image

from listings.models import Listing

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Populate database with sample users and listings"

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")

        # Clear existing data
        self.stdout.write("Clearing existing data...")
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create users
        self.stdout.write("Creating users...")
        users = self.create_users()

        # Create listings
        self.stdout.write("Creating listings...")
        self.create_listings(users)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated database with 50 users and 50 listings"
            )
        )

    def create_users(self):
        users = []
        realtors = []

        # Create 30 regular users and 20 realtors
        for i in range(30):
            user = User.objects.create_user(
                email=fake.unique.email(), name=fake.name(), password="testpass123"
            )
            users.append(user)

        for i in range(20):
            realtor = User.objects.create_realtor(
                email=fake.unique.email(), name=fake.name(), password="testpass123"
            )
            users.append(realtor)
            realtors.append(realtor)

        self.stdout.write(f"Created {len(users)} users (20 realtors, 30 regular users)")
        return realtors

    def create_sample_image(self):
        # Create a simple colored rectangle as placeholder
        img = Image.new("RGB", (800, 600), color=(73, 109, 137))
        img_io = io.BytesIO()
        img.save(img_io, format="JPEG")
        img_io.seek(0)
        return ContentFile(img_io.getvalue(), name="sample.jpg")

    def create_listings(self, realtors):
        states = [
            "California",
            "Texas",
            "Florida",
            "New York",
            "Pennsylvania",
            "Illinois",
            "Ohio",
            "Georgia",
            "North Carolina",
            "Michigan",
        ]

        home_types = ["House", "Condo", "Townhouse"]
        sale_types = ["For Sale", "For Rent"]

        for i in range(50):
            title = fake.sentence(nb_words=4).replace(".", "")
            slug = slugify(title) + f"-{i}"

            # Ensure unique slug
            while Listing.objects.filter(slug=slug).exists():
                slug = slugify(title) + f"-{random.randint(1000, 9999)}"

            listing = Listing(
                realtor=random.choice(realtors).email,
                title=title,
                slug=slug,
                address=fake.street_address(),
                city=fake.city(),
                state=random.choice(states),
                zipcode=fake.zipcode(),
                description=fake.paragraph(nb_sentences=5),
                price=random.randint(150000, 2000000),
                bathrooms=round(random.uniform(1.0, 5.0), 1),
                bedrooms=random.randint(1, 6),
                sale_type=random.choice(sale_types),
                home_type=random.choice(home_types),
                is_published=random.choice([True, False]),
            )

            # Add sample images
            listing.main_photo.save(
                f"main_{i}.jpg", self.create_sample_image(), save=False
            )
            listing.photo_1.save(
                f"photo1_{i}.jpg", self.create_sample_image(), save=False
            )
            listing.photo_2.save(
                f"photo2_{i}.jpg", self.create_sample_image(), save=False
            )
            listing.photo_3.save(
                f"photo3_{i}.jpg", self.create_sample_image(), save=False
            )

            listing.save()

        self.stdout.write("Created 50 listings")
