from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings
from . import process_data 
import os


def index(request):
  return render(request, 'submit.html') 


def upload(request):

  if request.method == 'POST':

    uploaded_file = request.FILES['file']
    destination_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    file_name = 'uploaded_file.xml'
    if not os.path.exists(destination_dir):
      os.makedirs(destination_dir)

    with open(os.path.join(destination_dir, file_name), 'wb+') as destination:
      for chunk in uploaded_file.chunks():
        destination.write(chunk)
    
    df = process_data.process()
    df_h = df.to_html(index=False)

    # for index, row in df.iterrows

    return render(request, 'table_data.html', {'df' : df})
  
  return HttpResponse('<h1>No File Uploaded</h1>')



  