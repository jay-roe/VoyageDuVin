import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Session, SessionWine
from .forms import WineScoreForm, UploadFileForm
from .utils import add_score_excel, create_workbook, handle_new_wines
from VoyageDuVin import settings


def index(request, session_name):
    session = get_object_or_404(Session, name=session_name.replace("_", " "))

    if request.method == "POST":
        form = WineScoreForm([], request.POST)
        if form.is_valid():
            add_score_excel(list(form.data.values())[1:], session)
            return HttpResponseRedirect(reverse('polls:thanks', args=[session_name]))
        else:  # Probably submitted from the raw html page
            add_score_excel(list(form.data.values())[1:], session.id)
            return HttpResponseRedirect(reverse('polls:thanks', args=[session_name]))

    # Get wines for the session with their order
    session_wines_qs = SessionWine.objects.filter(session=session).order_by('order')
    wines = [sw.wine for sw in session_wines_qs]
    wine_tags = ['name_dummy']
    for sw in session_wines_qs:
        tags_qs = sw.wine.tags.all()
        wine_tags.append(list(tags_qs))

    # Prepare context
    form = WineScoreForm(wines=wines)
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
        form = UploadFileForm(request.POST)
        if form.is_valid:
            handle_new_wines(request.POST["files"])
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