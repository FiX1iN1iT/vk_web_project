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

        self.stdout.write(self.style.SUCCESS('Parsing - DONE'))

        # Create fake users
        users = []
        for _ in range(num):
            while True:
                username = fake.user_name()
                if not User.objects.filter(username=username).exists() and not any(
                        user.username == username for user in users):
                    break
            email = fake.email()
            password = fake.password()

            users.append(User(username=username, email=email, password=password))

        self.stdout.write(self.style.SUCCESS('users - DONE'))

        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS('User objects - DONE'))

        users = User.objects.all()

        # Create fake user profiles
        profiles = [
            Profile(user=users[i])
            for i in range(num)
        ]

        self.stdout.write(self.style.SUCCESS('profiles - DONE'))

        Profile.objects.bulk_create(profiles)

        self.stdout.write(self.style.SUCCESS('Profile objects - DONE'))

        # Create fake tags
        tags = []
        for i in range(num):
            while True:
                name = fake.word()
                if not Tag.objects.filter(name=name).exists() and not any(
                        tag.name == name for tag in tags):
                    break

            tags.append(Tag(name=name))
            self.stdout.write(self.style.SUCCESS(i))

        self.stdout.write(self.style.SUCCESS('tags - DONE'))

        Tag.objects.bulk_create(tags)

        self.stdout.write(self.style.SUCCESS('Tag objects - DONE'))

        tags = Tag.objects.all()

        # Create fake questions
        questions = [
            Question(
                user=users[fake.random_int(min=0, max=num - 1)],
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(),
                tags=tags.order_by('?')[:fake.random_int(min=1, max=6)],
                created_at=fake.date_between(start_date='-1y', end_date='today')
            ) for _ in range(questions_amount)
        ]

        self.stdout.write(self.style.SUCCESS('questions - DONE'))

        Question.objects.bulk_create(questions)

        self.stdout.write(self.style.SUCCESS('Question objects - DONE'))

        # Create fake answers
        answers = []
        for _ in range(answers_amount):
            user = users[fake.random_int(min=0, max=num - 1)]
            question = Question.objects.order_by('?').first()
            content = fake.paragraph()
            created_at = fake.date_between(
                start_date=question.created_at,
                end_date='today'
            )
            status = fake.random_element(elements=('c', 'i'))

            answers.append(Answer(user=user, question=question, content=content, created_at=created_at, status=status))

        self.stdout.write(self.style.SUCCESS('answers - DONE'))

        Answer.objects.bulk_create(answers)

        self.stdout.write(self.style.SUCCESS('Answer objects - DONE'))

        # Create fake votes
        votes = []
        for _ in range(votes_amount):
            flag = fake.boolean()
            user = users[fake.random_int(min=0, max=num - 1)]
            question = None if flag else Question.objects.order_by('?').first()
            answer = None if not flag else Answer.objects.order_by('?').first()
            value = fake.random_element(elements=(-1, 1))

            votes.append(Vote(user=user, question=question, answer=answer, value=value))

        self.stdout.write(self.style.SUCCESS('votes - DONE'))

        Vote.objects.bulk_create(votes)

        self.stdout.write(self.style.SUCCESS('Vote objects - DONE'))

        self.stdout.write(self.style.SUCCESS(f"Successfully populated the database with fake data with ratio = {num}."))
