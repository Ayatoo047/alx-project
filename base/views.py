from django.shortcuts import render, redirect
from .forms import BlogForm
from .models import Blog, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
