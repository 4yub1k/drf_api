import pytest

from django.contrib.auth.models import User


pytestmark = pytest.mark.django_db

"""
Testing Poll API Models. (Read factories before tests)
"""

"""Poll Model Testing"""


def test_poll_question(poll_factory):
    """
    Test poll question.
    """
    poll = poll_factory()
    assert poll.question == "Beautiful places in the world?"
    assert poll.__str__() == "Beautiful places in the world?"

    poll = poll_factory(question="Test Question?", created_by=poll.created_by)
    assert poll.question == "Test Question?"


def test_poll_created_by(poll_factory):
    """
    Test User , Created_by.
    """
    poll = poll_factory()
    assert poll.created_by.username == "salahuddin"

    """
    Test New User.
    """
    user = User.objects.create_user(username="salah", password="test123pass")

    poll = poll_factory(question=poll.question, created_by=user)
    assert poll.created_by.username == "salah"


"""Option Model Testing"""


def test_option(option_factory):
    """
    Test option.
    """
    option = option_factory()
    assert option.option == "Turkey"


def test_option_poll(option_factory):
    """
    Test option is added to correct poll/question.
    """
    option = option_factory()
    assert option.poll.question == "Beautiful places in the world?"


"""Vote Model Testing"""


# Users for poll, and vote
def create_user(user_vote_factory):
    user_poll = user_vote_factory(username="testuser")
    user_vote = user_vote_factory(username="Salah_9")
    return user_poll, user_vote


def test_vote_poll(vote_factory, poll_factory, option_factory, user_vote_factory):
    """
    Test voted is added to question/poll.
    """
    user_poll, user_vote = create_user(user_vote_factory)

    poll = poll_factory(question="Longests river?", created_by=user_poll)
    vote = vote_factory(poll=poll, option=option_factory(), vote_by=user_vote)
    assert vote.poll.question == "Longests river?"


def test_vote_option(vote_factory, poll_factory, option_factory, user_vote_factory):
    """
    Test Voted the option.
    """
    user_poll, user_vote = create_user(user_vote_factory)

    poll = poll_factory(question="Longests river?", created_by=user_poll)
    vote = vote_factory(poll=poll, option=option_factory(), vote_by=user_vote)
    assert vote.option.option == "Turkey"


def test_vote_voted_by(vote_factory, poll_factory, option_factory, user_vote_factory):
    """
    Test Voted by user
    """
    user_poll, user_vote = create_user(user_vote_factory)

    poll = poll_factory(question="Longests river?", created_by=user_poll)
    vote = vote_factory(poll=poll, option=option_factory(), vote_by=user_vote)
    assert vote.vote_by.username == "Salah_9"
