import pytest

from django.urls import reverse


pytestmark = pytest.mark.django_db

# Run: pytest -rA
"""Test User Views"""


def test_user_register(client):
    """
    Register new user.
    """
    response = client.get(reverse("create_user"))
    assert response.json() == {"detail": 'Method "GET" not allowed.'}
    assert response.status_code == 405  # not allowed, means page is working

    json = {
        "username": "salah9",
        "email": "salah@salah.com",
        "password": "testpassword",
    }
    response = client.post(reverse("create_user"), json)
    assert response.json() == {"username": "salah9", "email": "salah@salah.com"}


def test_user_login_token(client):
    """
    Test User login and Response with token
    """
    json = {
        "username": "salah9",
        "email": "salah@salah.com",
        "password": "testpassword",
    }
    client.post(reverse("create_user"), json)  # Create user
    response = client.post(
        reverse("login_user"), {"username": "salah9", "password": "testpassword"}
    )
    assert (
        "token" in response.json()
    )  # {'token': 'c9385c2227e610666f53ace01f128f919c228f63'}


"""Test Poll Views"""


# Note: You can create a single fixture with Poll, option, and vote.
def test_poll_question(client, user_with_token):
    """
    Add and Delete, new question/poll.
    """

    response = client.get(
        reverse("list_create_poll"),
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert len(response.json()) == 0

    # Add Question/poll
    data = {"question": "This is test question for poll!?"}
    response = client.post(
        reverse("list_create_poll"),
        data=data,
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert response.json()["question"] == data["question"]
    assert response.json()["id"] == 1
    poll_id = response.json()["id"]

    # Delete the question.
    response = client.delete(
        reverse("detail_poll", kwargs={"id": poll_id}),
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert len(response.content) == 0


def test_option_poll(client, user_with_token, poll_factory):
    """
    Test Adding option to the question/poll.
    """

    # Add Option to the question.
    poll = poll_factory(
        created_by=user_with_token
    )  # You can't delete option of other polls.
    response = client.post(
        reverse("list_create_options", kwargs={"id": poll.id}),
        data={"option": "Turkey !"},
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert response.json()["option"] == "Turkey !"
    assert response.json()["id"] == 1
    option_id = response.json()["id"]

    # Delete option.
    response = client.delete(
        reverse("detail_option", kwargs={"id": poll.id, "option_id": option_id}),
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert len(response.content) == 0


def test_vote_poll(client, user_with_token, poll_factory, user_vote_factory):
    """
    Test Voting to the poll, or select the option.
    """
    # Add question
    poll = poll_factory(created_by=user_with_token)

    # Add Option to the question.
    response = client.post(
        reverse("list_create_options", kwargs={"id": poll.id}),
        data={"option": "True it is"},
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert response.json()["option"] == "True it is"
    option_id = response.json()["id"]

    # Select option and vote
    response = client.post(
        # id for poll, and option_id for option to select.
        reverse("create_vote", kwargs={"id": poll.id, "option_id": 1}),
        data={"option": "True it is", "vote_by": user_vote_factory().pk},
        HTTP_AUTHORIZATION=f"Token {user_with_token.auth_token.key}",
    )
    assert response.json()["id"] == option_id
