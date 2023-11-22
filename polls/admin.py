from django.contrib import admin

from .models import Tag, Wine, Session, UserScore, WineScore

admin.site.register(Tag)
admin.site.register(Wine)
admin.site.register(Session)
admin.site.register(UserScore)
admin.site.register(WineScore)
