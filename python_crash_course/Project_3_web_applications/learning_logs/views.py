from django.shortcuts import render
from .models import Topic


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, "learning_logs/index.html")


def topics(request):
    """Show all topics."""
    ts = Topic.objects.order_by("date_added")
    context = {"topics": ts}  # info: a dictionary --> keys are names in the templates to access the data
    return render(request, "learning_logs/topics.html", context)
