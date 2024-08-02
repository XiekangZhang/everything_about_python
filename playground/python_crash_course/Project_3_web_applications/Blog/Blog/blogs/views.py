from django.http import Http404
from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import BlogForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'blogs/index.html')


@login_required
def blogs(request):
    # show all blogs
    # blogs = BlogPost.objects.all()
    # blogs = BlogPost.objects.order_by("date_added")
    blogs = BlogPost.objects.filter(owner=request.user).order_by("date_added")
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)


@login_required
def new_blog(request):
    # add a new blog post
    if request.method != "POST":
        blogForm = BlogForm()
    elif request.method == "POST":
        blogForm = BlogForm(request.POST)
        if blogForm.is_valid():
            blog = blogForm.save(commit=False)
            blog.owner = request.user
            blog.save()
            return redirect("blogs:blogs")
    context = {"form": blogForm}
    return render(request, 'blogs/new_blog.html', context)


@login_required
def blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    if blog.owner != request.user:
        raise Http404
    context = {'blog': blog}
    return render(request, 'blogs/blog.html', context)


@login_required
def edit_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    if blog.owner != request.user:
        raise Http404

    if request.method != 'POST':
        blogForm = BlogForm(instance=blog)
    else:
        blogForm = BlogForm(request.POST, instance=blog)
        if blogForm.is_valid():
            blogForm.save()
        return redirect("blogs:blog", blog_id=blog_id)
    context = {"form": blogForm, 'blog': blog}
    return render(request, 'blogs/edit_blog.html', context)
