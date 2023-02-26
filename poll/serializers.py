from rest_framework import serializers
from .models import Poll, Option, Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        extra_kwargs = {"poll": {"read_only": True}, "option": {"read_only": True}}     # don't show during POST


class OptionSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False, source="vote_option")

    class Meta:
        model = Option
        fields = "__all__"


class PollSerializer(serializers.ModelSerializer):
    """Note: If you are not using related names in Model then it will access the models using model_set"""
    option = OptionSerializer(many=True, read_only=True, required=False, source="option_poll")
    """
    print(option):
        OptionSerializer(many=True, read_only=True):
        id = IntegerField(label='ID', read_only=True)
        option = CharField(max_length=100)
        poll = PrimaryKeyRelatedField(queryset=Poll.objects.all())
    """
    class Meta:
        model = Poll
        fields = ["id", "question", "option", "created_by", "created_on"]
        extra_kwargs = {"created_by": {"read_only": True}, "created_on": {"read_only": True}}
        # fields = "__all__"      # it will nest the serializer, add field automatically
