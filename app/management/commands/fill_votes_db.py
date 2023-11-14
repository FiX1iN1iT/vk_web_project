# from django.core.management import BaseCommand
# from faker import Faker
# from django.contrib.auth.models import User
#
# from app.models import Question, Answer, Vote, Tag
#
# fake = Faker()
#
#
# class Command(BaseCommand):
#     help = "Fills database with fake votes"
#
#     def add_arguments(self, parser):
#         parser.add_argument("num", type=int)
#
#     def handle(self, *args, **kwargs):
#         num = kwargs['num']
#         votes_amount = num * 200
#         questions_amount = num * 10
#         answers_amount = num * 100
#
#         self.stdout.write(self.style.SUCCESS('Parsing - DONE'))
#
#         # Users, Questions, Answers
#         users = User.objects.all()
#         questions = Question.objects.all()
#         answers = Answer.objects.all()
#
#         self.stdout.write(self.style.SUCCESS('Getting User, Question, Answer objects - DONE'))
#
#         # Create fake votes
#         votes = []
#         for i in range(votes_amount):
#             flag = fake.boolean()
#             user = users[fake.random_int(min=0, max=num - 1)]
#             question = None if flag else questions[fake.random_int(min=0, max=questions_amount - 1)]
#             answer = None if not flag else answers[fake.random_int(min=0, max=answers_amount - 1)]
#             value = fake.random_element(elements=(-1, 1))
#
#             votes.append(Vote(user=user, question=question, answer=answer, value=value))
#             self.stdout.write(self.style.ERROR(f'{i} votes - DONE'))
#
#         self.stdout.write(self.style.SUCCESS('votes - DONE'))
#
#         Vote.objects.bulk_create(votes)
#
#         self.stdout.write(self.style.SUCCESS('Vote objects - DONE'))
#
#         # Tags
#         tags = Tag.objects.all()
#
#         self.stdout.write(self.style.SUCCESS('Getting Tag objects - DONE'))
#
#         # Add tags to questions
#         for question in questions:
#             question.tags.set(tags.order_by('?')[:fake.random_int(min=1, max=6)])
#
#         self.stdout.write(self.style.SUCCESS('Tags set - DONE'))
#
#         self.stdout.write(self.style.SUCCESS(f"Successfully populated the database with fake data with ratio = {num}."))
