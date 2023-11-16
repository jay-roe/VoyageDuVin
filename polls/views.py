from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


def index(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            # put into excel
            return HttpResponseRedirect("/thanks")
    else:
        form = NameForm()

    return render(request, "polls/index.html", {"form": form})


def thanks(request):
    return render(request, "polls/thanks.html", {})
