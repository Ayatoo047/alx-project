from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Blog


def searchBlogs(request):
    """
        This function search for a blogpost using the author, body(content) and title of the blogpost.
        The search function is case insensitive
    """
     
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    blogs = Blog.objects.distinct().filter(
        Q(owner__username__icontains=search_query) |
        Q(body__icontains=search_query) |
        Q(title__icontains=search_query)
    )
    
    return blogs, search_query

def paginateBlogs(request, blogs, results):
    """
        This function paginates the first page of the first page, it shows the number
        of blogposts based on the parameter results
    """

    page = request.GET.get('page')
    # results = 3
    paginator = Paginator(blogs, results)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        blogs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        blogs = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    # projects = paginator.page(page)
    print(page, leftIndex, rightIndex)
    custom_range = range(leftIndex, rightIndex)
    return custom_range, blogs