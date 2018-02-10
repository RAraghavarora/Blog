# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink
from django.utils.text import slugify
# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length = 100, unique=True)
	slug = models.SlugField(max_length=100,unique = True)
	body = models.TextField()
	posted =models.DateField(db_index = True, auto_now_add=True)
	category=models.ForeignKey('blog.Category', on_delete=models.CASCADE,default='1')
	date = models.DateTimeField(auto_now_add=True)
	update= models.DateTimeField(auto_now=True)

	#def __unicode__(self):
	#	return self.title

	def save(self, *args, **kwargs):
		self.slug=slugify(self.title)
		super(Blog, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	#@permalink
	#def get_absolute_url(self):
	#	return ('view_blog_post', None, {'slug':self.slug})


class Category(models.Model):
	title =models.CharField(max_length=100, db_index=True)
	slug =models.SlugField(max_length=100, db_index=True)
	#def __unicode__(self):
	#	return '%s' %self.title

	#@permalink
	#def get_absolute_url(self):
	#	return ('view_blog_category', None, {'slug':self.slug})

	def save(self, *args, **kwargs):
		self.slug=slugify(self.title)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

#Review this again!	