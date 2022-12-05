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


def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("-date_added")  # info: - means sort the results in reverse order
    context = {"topic": topic,
               "entries": entries}  # info: a dictionary --> keys are names in the templates to access the data
    return render(request, "learning_logs/topic.html", context)