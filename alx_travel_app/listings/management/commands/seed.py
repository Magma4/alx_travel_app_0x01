import uuid
from django.core.management.base import BaseCommand
from listings.models import User, Listing
from faker import Faker

class Command(BaseCommand):
    help = 'Seed the database with sample listings data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create sample users if none exist
        if not User.objects.exists():
            self.stdout.write("Creating sample users...")
            for _ in range(5):
                User.objects.create(
                    user_id=uuid.uuid4(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),
                    password_hash=fake.sha256(),
                    phone_number=fake.phone_number(),
                    role=fake.random_element(elements=('guest', 'host', 'admin')),
                )

        # Retrieve or create a host user
        host_user = User.objects.filter(role='host').first()
        if not host_user:
            host_user = User.objects.create(
                user_id=uuid.uuid4(),
                first_name='Host',
                last_name='User',
                email='host@example.com',
                password_hash=fake.sha256(),
                role='host',
            )

        # Create sample listings
        self.stdout.write("Creating sample listings...")
        for _ in range(10):
            Listing.objects.create(
                listing_id=uuid.uuid4(),
                host=host_user,
                name=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                location=fake.address(),
                price_per_night=round(fake.random_number(digits=3, fix_len=False) + fake.pyfloat(left_digits=2, right_digits=2)),
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with sample data!'))