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

        # Create fake tags
        tags = []
        tag_names = set()
        for i in range(num):
            while True:
                name = fake.word() + str(fake.random_int(min=0, max=num - 1))
                if name not in tag_names:
                    break

            tag_names.add(name)
            tags.append(Tag(name=name))
            self.stdout.write(self.style.ERROR(f'{i} tags - DONE'))

        self.stdout.write(self.style.SUCCESS('tags - DONE'))

        Tag.objects.bulk_create(tags)

        self.stdout.write(self.style.SUCCESS('Tag objects - DONE'))

        # Create fake users
        users = []
        user_usernames = set()
        for i in range(num):
            while True:
                username = fake.user_name()
                if username not in user_usernames:
                    break
            email = fake.email()
            password = fake.password()

            user_usernames.add(username)
            users.append(User(username=username, email=email, password=password))
            self.stdout.write(self.style.ERROR(f'{i} users - DONE'))

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

        # Create fake questions
        questions = [
            Question(
                user=users[fake.random_int(min=0, max=num - 1)],
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(),
                created_at=fake.date_between(start_date='-1y', end_date='today')
            ) for _ in range(questions_amount)
        ]

        self.stdout.write(self.style.SUCCESS('questions - DONE'))

        Question.objects.bulk_create(questions)

        self.stdout.write(self.style.SUCCESS('Question objects - DONE'))

        questions = Question.objects.all()

        # Create fake answers
        answers = []
        for i in range(answers_amount):
            user = users[fake.random_int(min=0, max=num - 1)]
            question = questions[fake.random_int(min=0, max=questions_amount - 1)]
            content = fake.paragraph()
            created_at = fake.date_between(
                start_date=question.created_at,
                end_date='today'
            )
            status = fake.random_element(elements=('c', 'i'))

            answers.append(Answer(user=user, question=question, content=content, created_at=created_at, status=status))
            self.stdout.write(self.style.ERROR(f'{i} answers - DONE'))

        self.stdout.write(self.style.SUCCESS('answers - DONE'))

        Answer.objects.bulk_create(answers)

        self.stdout.write(self.style.SUCCESS('Answer objects - DONE'))

        answers = Answer.objects.all()

        # Create fake votes
        votes = []
        for i in range(votes_amount):
            flag = fake.boolean()
            user = users[fake.random_int(min=0, max=num - 1)]
            value = fake.random_element(elements=(-1, 1))
            if flag:
                question = None
                answer = answers[fake.random_int(min=0, max=answers_amount - 1)]
                answer.total_votes += value
                answer.save()
            else:
                answer = None
                question = questions[fake.random_int(min=0, max=answers_amount - 1)]
                question.total_votes += value
                question.save()

            votes.append(Vote(user=user, question=question, answer=answer, value=value))
            self.stdout.write(self.style.ERROR(f'{i} votes - DONE'))

        self.stdout.write(self.style.SUCCESS('votes - DONE'))

        Vote.objects.bulk_create(votes)

        self.stdout.write(self.style.SUCCESS('Vote objects - DONE'))

        # Tags
        tags = Tag.objects.all()

        self.stdout.write(self.style.SUCCESS('Getting Tag objects - DONE'))

        # Add tags to questions
        for i in range(questions_amount):
            questions[i].tags.set(tags.order_by('?')[:fake.random_int(min=1, max=6)])
            self.stdout.write(self.style.ERROR(f'{i} tags set - DONE'))

        self.stdout.write(self.style.SUCCESS('Tags set - DONE'))

        self.stdout.write(self.style.SUCCESS(f"Successfully populated the database with fake data with ratio = {num}."))
