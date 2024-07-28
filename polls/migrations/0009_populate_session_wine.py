from django.db import migrations

def populate_session_wine(apps, schema_editor):
    WineScore = apps.get_model('polls', 'WineScore')
    SessionWine = apps.get_model('polls', 'SessionWine')

    for wine_score in WineScore.objects.all():
        session_wine = SessionWine.objects.filter(session=wine_score.user_score.session, wine=wine_score.wine).first()
        wine_score.session_wine = session_wine
        wine_score.save()

class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_remove_session_wines_remove_wine_order_sessionwine_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_session_wine),
    ]