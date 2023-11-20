import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import NameForm
from .utils import add_score, create_workbook
from VoyageDuVin import settings

import json

def index(request):
    if request.method == "POST":
        #print(request.body.get("name"))
        body = json.loads(request.body)
        print(body.get("name"))
        print(body.get('scores'))
        add_score([body.get("name")] + body.get('scores'))
        return redirect("/api/thanks")
        #form = NameForm(request.POST)
        #if form.is_valid():
            #add_score(list(form.data.values())[1:])
            #return HttpResponseRedirect("/thanks")
    else:
        form = NameForm()

    return render(request, "polls/index.html", {"form": form})


def thanks(request):
    return render(request, "polls/thanks.html", {})


def secret(request):
    return render(request, "polls/secret.html", {})


def download_results(request):
    if not (os.path.isfile(os.path.join(settings.MEDIA_ROOT, "results.xlsx"))):
        create_workbook()

    file = open(os.path.join(settings.MEDIA_ROOT, "results.xlsx"), 'rb')
    response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=results.xlsx"

    return response


def delete_results(request):
    if request.method == "POST":
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, "results.xlsx")):
            os.remove(os.path.join(settings.MEDIA_ROOT, "results.xlsx"))

        return render(request, "polls/secret_delete.html", {})

    return HttpResponseRedirect("/api/thanks")  # You only get here if you're a bitch
