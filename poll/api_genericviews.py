from rest_framework import generics
from rest_framework.views import APIView
from .serializers import PollSerializer, OptionSerializer, VoteSerializer, UserSerializer
from .models import Poll, Option
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from rest_framework.exceptions import NotFound, ValidationError
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

"""
For Detail About views: https://www.geeksforgeeks.org/class-based-views-django-rest-framework/
"""

# class ListPoll(ListAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


class ListCreatePoll(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def post(self, request):
        question = request.data.get("question")
        created_by = self.request.user.id
        data = {"question": question, "created_by": created_by}
        serializer = PollSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                raise ValidationError("Already Voted !")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailPoll(generics.RetrieveDestroyAPIView):
    lookup_field = "id"
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs.get("id"))

        if not request.user == poll.created_by:
            raise PermissionDenied("You are not allowed to delete this")
        return super().destroy(self, request, *args, **kwargs)


class CreateVote(generics.CreateAPIView):

    def post(self, request, id, option_id):
        """
        url: polls/<int:id>/options/<int:option_id>/vote/
        Suppose you have more then one parameters, then modify post else send JSON required fields in request body.
        Here we want to recieve {'voted_by': voted_by} from user.
        """
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
    serializer_class = OptionSerializer

    def get_queryset(self):
        queryset = Option.objects.filter(poll_id=self.kwargs["id"])

        if not queryset:
            raise NotFound("Not found !")
        return queryset

    def post(self, request, id):
        option = request.data.get("option")  # request.data is similar to request.POST/GET
        data = {"poll": id, "option": option}
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                raise ValidationError("Already Added !")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailOption(generics.RetrieveDestroyAPIView):
    serializer_class = OptionSerializer
    # by default get_object use pk/lookupfields, to get the item, but you want to pass multi paramter modify get_object
    # instead of queryset.
    # use get_object for detailed view, get_queryset for List view.

    def get_object(self):
        return Option.objects.get(poll_id=self.kwargs["id"], id=self.kwargs["option_id"])

    def destroy(self, request, *args, **kwargs):
        option = self.get_object()

        if not request.user == option.poll.created_by:
            raise PermissionDenied("You are not allowed to delete this")
        return super().destroy(self, request, *args, **kwargs)


class CreateUser(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginUser(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user to get token.
        user = authenticate(username=username, password=password)

        if user:
            return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong username/password."}, status=status.HTTP_200_OK)
