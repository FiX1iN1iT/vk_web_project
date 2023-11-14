from django.core.management import BaseCommand
from django.contrib.auth.models import User

from app.models import Question, Answer, Profile, Tag, Vote


class Command(BaseCommand):
    help = "Clears database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Start delete - DONE'))

        # Delete fake users
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('User objects deleted - DONE'))

        # Delete fake user profiles
        Profile.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Profile objects deleted - DONE'))

        # Delete fake tags
        Tag.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Tag objects deleted - DONE'))

        # Create fake questions
        Question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Question objects deleted - DONE'))

        # Create fake answers
        Answer.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Answer objects deleted - DONE'))

        # Create fake votes
        Vote.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Vote objects deleted - DONE'))

        self.stdout.write(self.style.SUCCESS(f"Successfully cleared all data."))
