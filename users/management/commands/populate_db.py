import io
import secrets  # Use instead of random for security

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from listings.models import Listing
from users.models import UserAccount as User

fake = Faker()


class Command(BaseCommand):
    help = "Populate database with sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            type=str,
            default="testpass123",
            help="Password for created users (default: testpass123)",
        )

    def handle(self, *args, **options):
        password = options["password"]

        # Clear existing data
        if self.confirm_action(
            "This will delete all existing users and listings. Continue?"
        ):
            User.objects.all().delete()
            Listing.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared existing data"))

        # Create users
        users = []
        realtors = []

        try:
            # Create regular users
            self.stdout.write("Creating users...")
            for i in range(30):
                user = User.objects.create_user(
                    email=fake.unique.email(), name=fake.name(), password=password
                )
                users.append(user)

            # Create realtors
            for i in range(20):
                realtor = User.objects.create_realtor(
                    email=fake.unique.email(), name=fake.name(), password=password
                )
                users.append(realtor)
                realtors.append(realtor)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {len(users)} users ({len(realtors)} realtors)"
                )
            )

            # Create listings
            self.stdout.write("Creating listings...")

            states = [
                "AL",
                "AK",
                "AZ",
                "AR",
                "CA",
                "CO",
                "CT",
                "DE",
                "FL",
                "GA",
                "HI",
                "ID",
                "IL",
                "IN",
                "IA",
                "KS",
                "KY",
                "LA",
                "ME",
                "MD",
                "MA",
                "MI",
                "MN",
                "MS",
                "MO",
                "MT",
                "NE",
                "NV",
                "NH",
                "NJ",
                "NM",
                "NY",
                "NC",
                "ND",
                "OH",
                "OK",
                "OR",
                "PA",
                "RI",
                "SC",
                "SD",
                "TN",
                "TX",
                "UT",
                "VT",
                "VA",
                "WA",
                "WV",
                "WI",
                "WY",
            ]

            sale_types = ["For Sale", "For Rent"]
            home_types = ["House", "Condo", "Townhouse"]

            listings_created = 0
            for i in range(100):
                title = fake.sentence(nb_words=4)[:-1]  # Remove period
                slug = slugify(title)

                # Ensure unique slug using secure random
                while Listing.objects.filter(slug=slug).exists():
                    slug = slugify(title) + f"-{secrets.randbelow(9000) + 1000}"  # nosec B311

                listing = Listing(
                    realtor=secrets.choice(realtors).email,  # nosec B311
                    title=title,
                    slug=slug,
                    address=fake.street_address(),
                    city=fake.city(),
                    state=secrets.choice(states),  # nosec B311
                    zipcode=fake.zipcode(),
                    description=fake.paragraph(nb_sentences=5),
                    price=secrets.randbelow(1850000) + 150000,  # nosec B311
                    bathrooms=round(secrets.randbelow(40) / 10 + 1.0, 1),  # nosec B311
                    bedrooms=secrets.randbelow(5) + 1,  # nosec B311
                    sale_type=secrets.choice(sale_types),  # nosec B311
                    home_type=secrets.choice(home_types),  # nosec B311
                    is_published=secrets.choice([True, False]),  # nosec B311
                )

                try:
                    listing.save()
                    listings_created += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to create listing: {e}")
                    )

            self.stdout.write(
                self.style.SUCCESS(f"Created {listings_created} listings")
            )
            self.stdout.write(
                self.style.SUCCESS("Database populated successfully!")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error populating database: {e}")
            )

    def confirm_action(self, message):
        """Ask user for confirmation"""
        response = input(f"{message} (y/N): ")
        return response.lower() in ["y", "yes"]
