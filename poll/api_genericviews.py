from rest_framework import generics
from rest_framework.views import APIView
from .serializers import PollSerializer, OptionSerializer, VoteSerializer, UserSerializer
from .models import Poll, Option
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import status
# from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework.exceptions import NotFound, ValidationError
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.db.models import Count
from rest_framework.decorators import api_view

"""
For Detail About views: https://www.geeksforgeeks.org/class-based-views-django-rest-framework/
"""

# class ListPoll(ListAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


class ListCreatePoll(generics.ListCreateAPIView):
    """
    list all question with options, votes.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @extend_schema(summary="List all polls")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Add new poll/question.",
        description="Add new poll.",
        examples=[
            OpenApiExample(
                "Example 1",
                value={"question": "Most Beautiful Island in world?"},
                request_only=True
            ),
        ]
    )
    def post(self, request):
        question = request.data.get("question")
        created_by = self.request.user.id
        data = {"question": question, "created_by": created_by}
        serializer = PollSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                raise ValidationError("Already Voted/Created !")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailPoll(generics.RetrieveDestroyAPIView):
    """
    Get or Delete the question by ID.
    """
    lookup_field = "id"
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @extend_schema(summary="Get poll by ID")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=self.kwargs.get("id"))

        if not request.user == poll.created_by:
            raise PermissionDenied("You are not allowed to delete this")
        return super().destroy(self, request, *args, **kwargs)


class CreateVote(generics.CreateAPIView):
    """
    Add vote to the question.
    """
    serializer_class = VoteSerializer   # for spectacular

    @extend_schema(
        summary="Add vote to poll.",
    )
    def post(self, request, id, option_id):
        # url: polls/<int:id>/options/<int:option_id>/vote/
        # Suppose you have more then one parameters, then modify post else send JSON required fields in request body.
        # Here we want to recieve {'voted_by': voted_by} from user.

        vote_by = request.data.get("vote_by")  # request.data is similar to request.POST/GET
        data = {'option': option_id, 'poll': id, 'vote_by': vote_by}
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                raise ValidationError("Already Voted !")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # polls/<int:id>/options/<int:option_id>/vote/
    # {'id': 4, 'option_id': 8}
    # def post(self, request, *args, **kwargs):
    #     print(self.kwargs)
    #     return super().post(request, *args, **kwargs)


class ListCreateOption(generics.ListCreateAPIView):
    """
    List or Add new options.
    """
    serializer_class = OptionSerializer

    def get_queryset(self):
        queryset = Option.objects.filter(poll_id=self.kwargs["id"])

        if not queryset:
            raise NotFound("Not found !")
        return queryset

    @extend_schema(summary="Get options for poll.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Add new options.",
        description="Add the options using the option id, and the id of question/poll.",
        examples=[
            OpenApiExample(
                "Example 1",
                value={"option": "Your Option."},
                request_only=True
            ),
        ]
    )
    def post(self, request, id):
        option = request.data.get("option")  # request.data is similar to request.POST/GET
        data = {"poll": id, "option": option}
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            poll = get_object_or_404(Poll, id=self.kwargs["id"])
            if not request.user == poll.created_by:
                raise PermissionDenied("You are not allowed to Add Options")
            try:
                serializer.save()
            except IntegrityError:
                raise ValidationError("Already Added !")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailOption(generics.RetrieveDestroyAPIView):
    """
    Creates and Delete the Option using the option id, and the id of question/poll.
    """
    serializer_class = OptionSerializer
    # by default get_object use pk/lookupfields, to get the item, but you want to pass multi paramter modify get_object
    # instead of queryset.
    # use get_object for detailed view, get_queryset for List view.

    def get_object(self):
        return get_object_or_404(Option, poll_id=self.kwargs["id"], id=self.kwargs["option_id"])

    @extend_schema(summary="Get option by ID")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # @extend_schema(
    #     summary="Delete the Option.",
    #     description="Delete the Option using the option id, and the id of question/poll.",
    #     examples=[OpenApiExample("test", value={"adsd"})]
    # )
    def destroy(self, request, *args, **kwargs):
        option = self.get_object()

        # Only user who created the poll can delete the options.
        if not request.user == option.poll.created_by:
            print(request.user, option.poll.created_by)
            raise PermissionDenied("You are not allowed to delete this")
        return super().destroy(self, request, *args, **kwargs)


class CreateUser(generics.CreateAPIView):
    """
    User Registration. Provide username, email and password.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginUser(APIView):
    """
    User Login. Post username and password, Return response with token: <token>
    """
    permission_classes = ()
    serializer_class = UserSerializer   # for spectacular

    @extend_schema(
        summary="Returns token",
        examples=[
            OpenApiExample(
                "Example 1",
                value={"username": "salah9", "password": "9salah@test"},
                request_only=True
            ),
            OpenApiExample(
                "Example 1",
                value={"token": "f27615dc00ee4c2403b39a65bcf431737c3135de"},
                response_only=True
            )
        ]
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user to get token.
        user = authenticate(username=username, password=password)

        if user:
            return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong username/password."}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Plots of poll {poll_id}",
)
@api_view(['GET'])
def plotview(request, poll_id):
    # votes = Vote.objects.filter(poll_id=poll_id).values("poll_id").annotate(total=Count("vote_by_id"))
    poll = get_object_or_404(Poll, id=poll_id)
    option = poll.option_poll.all().values("option")
    votes = poll.vote_poll.all().values("option_id").annotate(total=Count("vote_by_id"))
    # votes = poll.vote_poll.all().values("option_id").annotate(total=Count("vote_by_id"), question1=Value(poll.question,
    # output_field=CharField()))
    # print(option)
    from json import dumps
    # javascript json cries over single and double quotations.
    # print(dumps(list(votes)))     [{"option_id": 13, "total": 3}, {"option_id": 14, "total": 1}]
    # print(list(votes))            [{'option_id': 13, 'total': 3}, {'option_id': 14, 'total': 1}
    return render(
        request,
        "poll/plot.html",
        {
            "plotvalue": dumps(list(votes)),
            "option": dumps(list(option)),
            "question": poll.question
        }
    )
