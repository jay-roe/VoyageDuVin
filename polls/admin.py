from django.contrib import admin
from .models import Tag, Wine, Session, UserScore, WineScore, SessionWine

class SessionWineInline(admin.TabularInline):
    model = SessionWine
    extra = 1  # Number of extra forms to display
    min_num = 1  # Minimum number of forms required
    can_delete = True  # Allow deleting of inlines

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

class WineAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'full_name', 'variety', 'region', 'alcohol_content', 'sweetness', 'color', 'price')
    list_filter = ('variety', 'region', 'color')
    search_fields = ('short_name', 'full_name', 'variety', 'region')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = ('date',)
    search_fields = ('name',)
    inlines = [SessionWineInline]  # Add the inline to the Session admin

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('session', 'name')
    list_filter = ('session',)
    search_fields = ('name',)

class WineScoreAdmin(admin.ModelAdmin):
    list_display = ('user_score', 'session_wine', 'score')
    list_filter = ('user_score', 'session_wine')
    search_fields = ('user_score__name', 'session_wine__wine__short_name')

class SessionWineAdmin(admin.ModelAdmin):
    list_display = ('session', 'wine', 'order')
    list_filter = ('session', 'wine')
    search_fields = ('session__name', 'wine__short_name')

admin.site.register(Tag, TagAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(UserScore, UserScoreAdmin)
admin.site.register(WineScore, WineScoreAdmin)
admin.site.register(SessionWine, SessionWineAdmin)

