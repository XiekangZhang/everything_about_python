from django.shortcuts import redirect, render

from .models import Topic
from .forms import TopicForm


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


def new_topic(request):
    """Add a new topic."""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            # INFO: redirect() takes in the name of a view and redirects the user to the view.
            return redirect("learning_logs:topics")

    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)
