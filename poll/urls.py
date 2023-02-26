from django.urls import path
from .api_genericviews import ListCreatePoll, ListCreateOption,\
    CreateVote, DetailPoll, DetailOption, CreateUser, LoginUser
# from .api_genericviews import ListPoll, ListOption, CreateVote, DetailPoll, CreatePoll

urlpatterns = [
    # path("polls/", ListPoll.as_view(), name="list_poll"),
    path("polls/", ListCreatePoll.as_view(), name="list_create_poll"),
    path("polls/<int:id>/", DetailPoll.as_view(), name="detail_poll"),
    path("polls/<int:id>/options/", ListCreateOption.as_view(), name="list_create_options"),
    path("polls/<int:id>/options/<int:option_id>/", DetailOption.as_view(), name="detail_option"),
    # path("options/", ListOption.as_view(), name="list_options"),
    path("polls/<int:id>/options/<int:option_id>/vote/", CreateVote.as_view(), name="create_vote"),

    path("users/", CreateUser.as_view(), name="create_user"),
    path("login/", LoginUser.as_view(), name="login_user"),
]
