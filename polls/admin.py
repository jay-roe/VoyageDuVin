from django.contrib import admin

from .models import Tag, Wine, Session, UserScore, WineScore, SessionWine

class SessionWineInline(admin.TabularInline):
    model = SessionWine
    extra = 1  # Number of extra forms to display
    min_num = 1  # Minimum number of forms required
    can_delete = True  # Allow deleting of inlines

class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = ('date',)
    search_fields = ('name',)
    inlines = [SessionWineInline]  # Add the inline to the Session admin

admin.site.register(Tag)
admin.site.register(Wine)
admin.site.register(Session, SessionAdmin)
admin.site.register(UserScore)
admin.site.register(WineScore)
admin.site.register(SessionWine)

