from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True, blank=True)
    value = models.IntegerField()

    def __str__(self):
        return f"'{self.user.username}' voted on '{self.question.title}'"


class QuestionManager(models.Manager):
    def tagged(self, tag_name):
        return self.filter(tags__name=tag_name)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=256)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()

    STATUS_CHOICES = [
        ('c', 'correct'),
        ('i', 'incorrect'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')

    def __str__(self):
        return f"Answer to '{self.question.title}' from '{self.user.username}'"


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
