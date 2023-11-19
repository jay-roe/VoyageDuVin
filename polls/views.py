from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from .utils import add_score


def index(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            add_score(list(form.data.values())[1:])
            return HttpResponseRedirect("/thanks")
    else:
        form = NameForm()

    return render(request, "polls/index.html", {"form": form})


def thanks(request):
    return render(request, "polls/thanks.html", {})
