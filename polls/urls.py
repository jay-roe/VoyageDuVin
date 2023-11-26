from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path("<int:session>", views.index, name="index"),
    path("thanks", views.thanks, name="thanks"),
    path("secret", views.secret, name="secret"),
    path("secret/add", views.add_wines, name="add_wines"),
    path("secret/download", views.download_results, name="download_results"),
    path("secret/delete", views.delete_results, name="delete_results"),
    path("vins", views.vins, name="vins")
]
