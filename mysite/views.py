#View that will be called by the main urls.py file
from django.shortcuts import render

def default(request):
	return render(request,'project/default.html')