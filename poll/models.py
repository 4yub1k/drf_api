from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Poll(models.Model):
    question = models.CharField(max_length=200, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question


class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name="option_poll", on_delete=models.CASCADE)
    option = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.option


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name="vote_poll", on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name="vote_option", on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.option.option
