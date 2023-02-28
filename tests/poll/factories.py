import factory

from django.contrib.auth.models import User
from poll.models import Poll, Option, Vote


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # id = 1  # Not required, just for readability.
    username = "salahuddin"
    email = "test@test.com"
    password = "blacksky"
    is_active = True
    is_superuser = False


class UserVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "salahuddin_99"
    email = "test1@test.com"
    password = "blacksky99"
    is_active = True
    is_superuser = False


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll

    question = "Beautiful places in the world?"
    created_by = factory.SubFactory(UserFactory)


class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option

    poll = factory.SubFactory(PollFactory)
    option = "Turkey"


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    poll = factory.SubFactory(PollFactory)
    option = factory.SubFactory(OptionFactory)
    vote_by = factory.SubFactory(UserVoteFactory)
