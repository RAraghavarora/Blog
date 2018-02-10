# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import PostForm,RegistrationForm
#from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Blog, Category
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import logout,login
#from app.forms import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User


def index(request):
	print request.user.username
	context={'categories':Category.objects.all(),'posts':Blog.objects.all(), 'username':request.user.username}
	return render(request,'blog/index.html', context)

def view_post(request, slug):
	context = {'post':get_object_or_404(Blog, slug=slug)}

	return render(request,'blog/view_post.html',context)


def view_category(request, slug):
	category = get_object_or_404(Category, slug=slug)
	context = {'category':category, 'posts':Blog.objects.filter(category = category)}
	return render(request,'blog/view_category.html', context)

def post_new(request):

	if request.method=='POST':
		form =PostForm(request.POST)
		if form.is_valid():
			blog=form.save(commit=False)
			blog.save()
			context = {'post':get_object_or_404(Blog, slug=blog.slug)}

			return render(request,'blog/view_post.html',context)

	else:
		form = PostForm()

	context={'form':form}
	return render(request, 'blog/post_edit.html',context)

def post_edit(request,slug):
	post = get_object_or_404(Blog, slug=slug)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			print "YES"
			post = form.save(commit=False)
			post.date=timezone.now()
			post.save()
			context={'post':post, 'slug':post.slug}
			return render(request, 'blog/view_post.html', context)

	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html',{'form':form})

def logout_page(request):
	#View for logout page, it will perform the operations we need to perform
	#before the user is finally logged out.
	logout(request)
	return HttpResponseRedirect('/')


def register_page(request):
	if request.method=='POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user=User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
			login(request,user)
			return HttpResponseRedirect('/blog')
	form=RegistrationForm()
	return render(request, 'registration/register.html', {'form':form})
