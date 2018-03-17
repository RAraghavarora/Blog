# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length = 100, unique=True)
	slug = models.SlugField(max_length=100,unique = True)
	body = models.TextField()
	img=models.ImageField(default='a.jpg')
	posted =models.DateField(db_index = True, auto_now_add=True)
	category=models.ForeignKey('blog.Category', on_delete=models.CASCADE,default='1')
	date = models.DateTimeField(auto_now_add=True)
	update= models.DateTimeField(auto_now=True)

#revisit on_delete .
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
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	birth_date=models.DateField(null=True, blank=True)
	followers=models.ManyToManyField(User,related_name='following',symmetrical=False)#list of followers


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created :
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
