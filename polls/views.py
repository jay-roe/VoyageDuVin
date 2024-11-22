import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Session, SessionWine, UserScore, WineScore, Wine
from .forms import WineScoreForm, UploadFileForm
from .utils import add_score_excel, create_workbook, handle_new_wines, handle_urls
from VoyageDuVin import settings


def index(request, session_name):
    session = get_object_or_404(Session, name=session_name.replace("_", " "))

    if request.method == "POST":
        session_wines_qs = SessionWine.objects.filter(session=session).order_by('order')
        wines = [sw.wine for sw in session_wines_qs]
        form = WineScoreForm(wines=wines, data=request.POST)
        if form.is_valid():
            user_score = UserScore.objects.create(session=session, name=form.cleaned_data['name'])
            for field_name, value in form.cleaned_data.items():
                if field_name.startswith('wine_'):
                    wine_id = int(field_name.split('_')[1])
                    session_wine = get_object_or_404(SessionWine, session=session, wine_id=wine_id)
                    WineScore.objects.create(user_score=user_score, session_wine=session_wine, score=value)
            return HttpResponseRedirect(reverse('polls:thanks', args=[session_name]))

    else:  # Probably submitted from the raw html page
        wines_qs = SessionWine.objects.filter(session=session).order_by('order')
        wines = [sw.wine for sw in wines_qs]
        form = WineScoreForm(wines=wines)

    # Prepare context
    wine_tags = ['name_dummy']
    for sw in wines_qs:
        tags_qs = sw.wine.tags.all()
        wine_tags.append(list(tags_qs))

    wines.insert(0, 'name_dummy')
    form_data = zip(form, wines, wine_tags)
    return render(request, "polls/index.html", {"form": form_data, "session_name": session_name})

def thanks(request, session_name):
    return render(request, "polls/thanks.html", {"session_name": session_name})

def fuckyou(request):
    return render(request, "polls/fuckyou.html", {})

def secret(request):
    return render(request, "polls/secret.html", {})

def add_wines(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if 'files' in request.FILES:
                # Handle file upload
                uploaded_file = request.FILES["files"]
                handle_new_wines(uploaded_file)
            elif 'urls' in request.POST:
                # Handle comma-separated URLs
                urls = request.POST["urls"]
                url_list = [url.strip() for url in urls.split(",")]
                handle_urls(url_list)
            return HttpResponseRedirect("add")
    else:
        form = UploadFileForm()
    return render(request, "polls/secret_add.html", {})
    


def download_results(request):
    # Get all session IDs
    session_ids = Session.objects.values_list('id', flat=True)

    if not (os.path.isfile(os.path.join(settings.MEDIA_ROOT, "results.xlsx"))):
        create_workbook(session_ids)

    file = open(os.path.join(settings.MEDIA_ROOT, "results.xlsx"), 'rb')
    response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=results.xlsx"

    return response


def delete_results(request):
    if request.method == "POST":
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, "results.xlsx")):
            os.remove(os.path.join(settings.MEDIA_ROOT, "results.xlsx"))

        return render(request, "polls/secret_delete.html", {})

    return HttpResponseRedirect("fuckyou")  # You only get here if you're a bitch


def vins(request):
    return render(request, "polls/vins.html", {})


def session_scores(request, session_name):
    session = get_object_or_404(Session, name=session_name.replace("_", " "))
    session_wines = SessionWine.objects.filter(session=session).order_by('order')
    users = UserScore.objects.filter(session=session)

    # Prepare data for the table
    wines = [sw.wine for sw in session_wines]
    scores = {}
    for user in users:
        user_scores = WineScore.objects.filter(user_score=user)
        scores[user.name] = {ws.session_wine.wine.id: ws.score for ws in user_scores}

    return render(request, 'polls/session_scores.html',
                  {'session': session, 'wines': wines, 'scores': scores, 'users': users})

def user_scores(request, user_name):
    user_scores = UserScore.objects.filter(name=user_name)
    if not user_scores.exists():
        return render(request, 'polls/user_scores.html', {'user_name': user_name, 'scores': [], 'user_exists': False})

    user = user_scores.first()
    scores_by_session = {}
    wine_preferences = {}
    total_scores = 0
    score_count = 0

    for us in user_scores:
        wine_scores = WineScore.objects.filter(user_score=us)
        scores_by_session[us.session] = wine_scores

        for ws in wine_scores:
            wine = ws.session_wine.wine
            total_scores += ws.score
            score_count += 1
            if wine.variety not in wine_preferences:
                wine_preferences[wine.variety] = {'count': 0, 'total_score': 0}
            wine_preferences[wine.variety]['count'] += 1
            wine_preferences[wine.variety]['total_score'] += ws.score

    if score_count > 0:
        average_score = total_scores / score_count
    else:
        average_score = 0

    for variety in wine_preferences:
        wine_preferences[variety]['average_score'] = wine_preferences[variety]['total_score'] / wine_preferences[variety]['count']

    return render(request, 'polls/user_scores.html', {
        'user_name': user_name,
        'scores_by_session': scores_by_session,
        'wine_preferences': wine_preferences,
        'average_score': average_score,
        'user_exists': True
    })


def wine_scores(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)
    filter_by = request.GET.get('filter_by', 'all')
    scores = []

    if filter_by == 'user':
        user_name = request.GET.get('user_name', '').strip()
        if user_name:
            user_scores = UserScore.objects.filter(name=user_name)
            scores = WineScore.objects.filter(user_score__in=user_scores, session_wine__wine=wine)
        else:
            scores = WineScore.objects.filter(session_wine__wine=wine)
    elif filter_by == 'session':
        session_name = request.GET.get('session_name', '').strip()
        if session_name:
            try:
                session = get_object_or_404(Session, name=session_name.replace("_", " "))
                session_wines = SessionWine.objects.filter(session=session, wine=wine)
                scores = WineScore.objects.filter(session_wine__in=session_wines)
            except:
                session = None
        else:
            scores = WineScore.objects.filter(session_wine__wine=wine)
    else:  # filter_by == 'all'
        scores = WineScore.objects.filter(session_wine__wine=wine)

    return render(request, 'polls/wine_scores.html', {'wine': wine, 'scores': scores, 'filter_by': filter_by})


def general_scores(request):
    sessions = Session.objects.all()
    users = UserScore.objects.values_list('name', flat=True).distinct()
    wines = Wine.objects.all()

    return render(request, 'polls/general_scores.html', {
        'sessions': sessions,
        'users': users,
        'wines': wines
    })

def wine_image(request, wine_id):
    try:
        wine = Wine.objects.get(id=wine_id)
        return HttpResponse(wine.image_content, content_type="image/jpeg")
    except Wine.DoesNotExist:
        return HttpResponse(status=404)