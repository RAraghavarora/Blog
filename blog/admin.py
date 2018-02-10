# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin#importing the command To register the models we create
from blog.models import Blog, Category#Importing the momdels we created

class BlogAdmin(admin.ModelAdmin):
	exclude = ['posted']#Automatically populated with the date it was created
	prepopulated_fields = {'slug' : ('title',)}#To automatically populate the slug field by the title name
	search_fields = ('title', 'body')

class CategoryAdmin(admin.ModelAdmin):
	exlude = ('slug',)
	prepopulated_fields = {'slug' : ('title',)}


#Doubt:Review again !!!


#Hint: Try to use a save function

# Register your models here.
admin.site.register(Blog,BlogAdmin)
admin.site.register(Category,CategoryAdmin)
#Just registered the models Blog and Category with the admin