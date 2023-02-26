from django.contrib import admin
from .models import Poll, Option, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass
