import pytest

from pytest_factoryboy import register
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .factories import (
    PollFactory,
    OptionFactory,
    VoteFactory,
    UserVoteFactory,
    UserFactory,
)


register(PollFactory)
register(OptionFactory)
register(VoteFactory)
register(UserVoteFactory)
register(UserFactory)


# Add user Using User Model
@pytest.fixture()
def user_with_token():
    user = User.objects.create_user(username="salahtest", password="passtest")
    Token.objects.create(user=user)
    # print(user.auth_token.key)    # a82edd6e94ad620e2dcee75a7872d26a3a9272e9
    # token = f"Token {user_with_token.auth_token.key}"
    return user


# Add User Using Factory
# @pytest.fixture()
# def factory_user_token():
#     user= UserFactory(username="salah123")
#     Token.objects.create(user=user)
#     return f"Token {user.auth_token.key}"
