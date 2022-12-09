from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import BlogPostForm


# Create your views here.
def home(request):
    blogs = BlogPost.objects.order_by("date_added")
    return render(request, 'blogs/home.html', {"blogs": blogs})


def add_blog(request):
    if request.method != "POST":
        form = BlogPostForm()
    else:
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:home')
    context = {"form": form}
    return render(request, 'blogs/add_blog.html', context)


def edit_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)

    if request.method != "POST":
        form = BlogPostForm(instance=blog)
    else:
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blogs:home")
    context = {"form": form, 'blog': blog}
    return render(request, "blogs/edit_blog.html", context)
