from django.core.management import BaseCommand
from faker import Faker
from django.contrib.auth.models import User

from app.models import Question, Answer, Profile, Tag, Vote

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data for your models"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']
        votes_amount = num * 200
        questions_amount = num * 10
        answers_amount = num * 100

        # Create fake user profiles
        profiles = [
            Profile(user=User(username=fake.user_name(), email=fake.email()))
            for _ in range(num)
        ]
        Profile.objects.bulk_create(profiles)

        # Create fake tags
        tags = [
            Tag(name=fake.word())
            for _ in range(num)
        ]
        Tag.objects.bulk_create(tags)

        profiles = Profile.objects.all()
        tags = Tag.objects.all()

        # Create fake votes
        votes = []
        for _ in range(votes_amount):
            flag = fake.boolean()
            user = profiles[fake.random_int(min=0, max=num - 1)].user
            question = None if flag else Question.objects.order_by('?').first()
            answer = None if not flag else Answer.objects.order_by('?').first()
            value = fake.random_element(elements=(-1, 1))

            votes.append(Vote(user, question, answer, value))

        Vote.objects.bulk_create(votes)

        # Create fake questions
        questions = [
            Question(
                user=profiles[fake.random_int(min=0, max=num - 1)].user,
                title=fake.sentence(nb_words=3),
                content=fake.paragraph(),
                created_at=fake.date_between(start_date='-1y', end_date='today')
            ) for _ in range(questions_amount)
        ]
        Question.objects.bulk_create(questions)

        # Create fake answers
        answers = []
        for _ in range(answers_amount):
            user = profiles[fake.random_int(min=0, max=num - 1)].user
            question = Question.objects.order_by('?').first()
            content = fake.paragraph()
            created_at = fake.date_between(
                start_date=question.created_at,
                end_date='today'
            )
            status = fake.random_element(elements=('c', 'i'))

            answers.append(Answer(user, question, content, created_at, status))

        Answer.objects.bulk_create(answers)

        # Add tags to questions
        for question in Question.objects.all():
            question.tags.set(tags.order_by('?')[:fake.random_int(min=1, max=6)])
