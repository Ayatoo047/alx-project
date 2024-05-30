from django.shortcuts import render, redirect
from .forms import BlogForm
from .models import Blog, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . utils import searchBlogs, paginateBlogs


def error_404_view(request, exception):
    """
        This view overide the 404 page of django
    """
    data = {"name": "ThePythonDjango.com"}
    return render(request,'base/404.html', data)


def all_blogs(request):
    """
        This view return all of the blogposts, showing 5 item on each page, according to the
        last parameter of the paginateBlogs fucntion (5).It also get the queryset by the serach parameter.
    """
    blogs, search_query = searchBlogs(request)
    custom_range, blogs = paginateBlogs(request, blogs,5)

    print(blogs.number)
    context = {'blogs': blogs, 'search_query': search_query, 'custom_range': custom_range}

    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


@login_required(login_url='login')
def createBlogpost(request):
    """
        This view creates a blogpost. It implement the django model form
        for creation of the blog. It show a message on success and failure
    """
    page = 'create'

    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blogs = form.save(commit=False)
            blogs.owner = request.user
            blogs.save()
            messages.success(request, 'Blogpost Created')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Inputs, Please enter valid values')
            return redirect('create')


    context = {'form': form, 'page':page}
    return render(request, 'base/add.html', context)


@login_required(login_url='login')
def updateBlogpost(request, pk):
    """
        This view update a blogpost. It uses a customized html form
        for updating of the blog and show a message on success. The two types
        forms (django form and html) to show the ability to use dynamic method of getting data
    """

    blog = Blog.objects.filter(id=pk).first()
   
    if request.method == 'POST':
        body = request.POST['body']
        snippet = request.POST['snippet']
        title = request.POST['title']

        if body != '' and title != '':
            blog.body = body
            blog.snippet = snippet
            blog.title = title
            blog.save()
            messages.success(request, 'Blogpost Update')
            return redirect('blogpost', blog.id)

        else:
            messages.error(request, 'Feild can not be empty')
            return redirect('update', blog.id)
    
    context = {'blog': blog}
    return render(request, 'base/add.html', context)


def singleBlogpost(request, pk):
    """
        This view a single a blogpost, showing its details. It also gets the comments
        under a particular blogpost. It allows an authenticated user to leave a comment 
        under a blogpost. Use must be logged in to create a post
    """

    blogs = Blog.objects.get(id=pk)
    comments =  blogs.comment_set.all()

    # if request.method == 'POST':
    #     Comment.objects.create(
    #         owner = request.user,
    #         blogs = blogs,
    #         body = request.POST.get('body')
    #     )
    #     return redirect('blogpost', pk=blogs.id)
    

    context = {'blogs': blogs, 'comments': comments}
    return render(request, 'base/details.html', context)


def delete(request, pk):
    """
        This view deletes a blogpost. 
    """

    blog = Blog.objects.get(id=pk)
    blog.delete()
    return redirect('home')

