from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path("secret/", views.secret, name="secret"),
    path("secret/add", views.add_wines, name="add_wines"),
    path("secret/download", views.download_results, name="download_results"),
    path("secret/delete", views.delete_results, name="delete_results"),
    path("secret/fuckyou", views.fuckyou, name="fuckyou"),
    path("vins", views.vins, name="vins"),
    path("<str:session_name>/", views.index, name="index"),
    path("<str:session_name>/thanks/", views.thanks, name="thanks"),
    path("session/<str:session_name>/scores/", views.session_scores, name="session_scores"),
    path("user/<str:user_name>/scores/", views.user_scores, name="user_scores"),
    path("wine/<int:wine_id>/scores/", views.wine_scores, name="wine_scores"),
    path("general/scores/", views.general_scores, name="general_scores"),  # New path for general scores
    path('wine-image/<int:wine_id>/', views.wine_image, name='wine_image'),

]
