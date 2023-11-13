from django.core.management import BaseCommand
from faker import Faker

from app.models import Question, Answer, Profile, Tag, Vote

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']
        authors = [
            Author(
                name=fake.first_name(), surname=fake.last_name(),
                birth_date=str(fake.date_between(start_date='-100y', end_date='-20y')),
                death_date=None if (fake.random_int() % 2 == 0) else
                str(fake.date_between(start_date='-19y', end_date='-1d'))
            ) for _ in range(num)
        ]
        Author.objects.bulk_create(authors)
        authors = Author.objects.all()
        authors_count = authors.count()
        books = [
            Book(
                title=fake.sentence(nb_words=3),
                author=authors[fake.random_int(min=0, max=authors_count - 1)],
                date_written=str(fake.date_between(start_date='-40y', end_date='-10y'))
            ) for _ in range(num*2)
        ]
        Book.objects.bulk_create(books)
