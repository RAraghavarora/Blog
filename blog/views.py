# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import PostForm,RegistrationForm
#from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Blog, Category,Profile
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login as auth_login, views as auth_views
#from django.contrib.auth import login as auth_login
#from app.forms import *
#from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.db.models import Q
from PIL import Image
import os
#Django.contrib.auth  ---------  authenticate() to authenticate if the specific user is logged in

@login_required
def index(request):
	#print request.user.username
	#a=list(Profile.objects.all())
	#print a.username   --------------   WRONG!
#	print a[0].user.username	----------- RIGHT!
	if request.GET:
		query=(request.GET.get("q"))
		#print query
		request.session['query']=query
		return redirect('blog:search')


	q=request.user
	#tr=authenticate(username='raghav',password='bitspilani')
	a=Profile.objects.get(user=q)
	#u=authenticate()

	list_following=list(q.following.all())
	l=len(list_following)

	context={'l':l,'list':list_following,'categories':Category.objects.all(),'followers':list(a.followers.all()),'posts':Blog.objects.all(), 'username':request.user.username,'user_profile':a}
	return render(request,'blog/index.html', context)

@login_required
def view_post(request, slug):
	context = {'post':get_object_or_404(Blog, slug=slug)}

	return render(request,'blog/view_post.html',context)


def view_category(request, slug):
	category = get_object_or_404(Category, slug=slug)
	context = {'category':category, 'posts':Blog.objects.filter(category = category)}
	return render(request,'blog/view_category.html', context)

@login_required
def post_new(request):

	if request.method=='POST':
		form =PostForm(request.POST,request.FILES)
		#print "IS_VALID"
		if form.is_valid():
			blog=form.save(commit=False)
			blog.author=Profile.objects.get(user=request.user)
			im=Image.open(blog.img)
			#print type(blog.img)
			'''fn , fext = os.path.splitext(im)
			im2= im.convert('RGB')
			im2.save('demo.jpg')'''
			blog.save()
			#print im.filename
			#print fn + '\n' + fext
			context = {'post':get_object_or_404(Blog, slug=blog.slug),'image':blog.img }

			return render(request,'blog/view_post.html',context)
		
	else:
		form = PostForm()

	context={'form':form}
	return render(request, 'blog/post_edit.html',context)

def post_edit(request,slug):
	#print slug
	post = get_object_or_404(Blog, slug=slug)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			#print "YES"
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
			auth_login(request,user)
			return HttpResponseRedirect('/blog')
	form=RegistrationForm()
	return render(request, 'registration/register.html', {'form':form})

def search(request):
	qlist=(Profile.objects.all())
	query=request.session['query']
	logged_in=request.user
	#print "qweoplksasdp;swiop"
	#query=(request.GET.get("q"))
	#print query
	if query:
		qlist = qlist.filter(user__username__icontains=query).filter(~Q(user=logged_in))
	qlist=list(qlist)
	list_names=[]
	pro=request.user
	a=0
	for i in qlist:
		list_names.append(i)
		
		a+=1
	if None:
		#print i.pk
		#print "Raghav"
		return redirect('blog:follow',pk=i.pk)
	context= {'list_names':list_names,'logged_in':pro}
	return render(request, 'blog/search.html', context)

def follow(request,pk):
	#print pk
	p=Profile.objects.get(pk=pk) #user we searched
	q= request.user #logged_in user
	#print q.username
	#print p.user.username
	p.followers.add(q)

	return redirect('blog:index')

def unfollow(request,pk):
	p=Profile.objects.get(pk=pk)
	q=request.user
	p.followers.remove(q)
	return redirect('blog:search')

def login(request):
	return redirect(auth_views.login)
