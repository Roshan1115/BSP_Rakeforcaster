from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from . import process_data 
import pandas as pd
import os


def index(request):
  return render(request, 'index.html') 

df_global = pd.DataFrame()  

def upload(request):
  global df_global
  if request.method == 'POST':

    uploaded_file = request.FILES['file']
    destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    file_name = 'uploaded_file.xml'
    if not os.path.exists(destination_dir):
      os.makedirs(destination_dir)

    with open(os.path.join(destination_dir, file_name), 'wb+') as destination:
      for chunk in uploaded_file.chunks():
        destination.write(chunk)
    
    df_global = process_data.process()
    return HttpResponse("success")

  return HttpResponse("<h1>No file uploade</h1>")


def upload_success(request):
  return render(request, 'table_data.html', {'df' : df_global})




