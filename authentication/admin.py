from django.contrib import admin
from .models import Tokens


# Register your models here.
@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    pass
