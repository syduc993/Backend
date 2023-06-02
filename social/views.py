import rest_framework.status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
from rest_framework import  permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
import requests
import time
import datetime
from django.db import models
from django.utils import timezone

import zipfile
import pandas as pd
import os
from pathlib import Path
import shutil
import warnings
import random
from django.core.files.storage import FileSystemStorage
import uuid
from .function import *

@api_view(['POST'])
def get_my_zip_file(request):
    try:
        in_memory_file_obj = request.FILES.get('file')
        name_xlsx = uuid.uuid4().hex.upper()[0:6] + '.xlsx'
        FileSystemStorage(location="try_Django/social/files_exel").save(name_xlsx, in_memory_file_obj)
        folder_path ='my_zip_'+str(random.randint(1, 99999))
        folder_path1 = 'try_Django/social/upload/'+folder_path+'/'
        os.mkdir(folder_path1)

        Tach_file_tang_truong(name_xlsx,folder_path1)

        shutil.make_archive (folder_path, 'zip', 'try_Django/social/upload/'+folder_path+'/')
        shutil.move(folder_path+'.zip', 'try_Django/social/upload/')
        shutil.rmtree('try_Django/social/upload/' + folder_path)
        os.remove('try_Django/social/files_exel/' + name_xlsx)

        message = {'Thongbao':'Thành công','data':folder_path+'.zip'}
        return Response(message,status=status.HTTP_200_OK)

    except:
        shutil.rmtree('try_Django/social/upload/' + folder_path)
        os.remove('try_Django/social/files_exel/' + name_xlsx)
        message = {'Thongbao':'Thất bại',}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_my_zip_file(request):
	name = request.data['Return_data']
	file_path = 'try_Django/social/upload/'+ name
	os.remove(file_path)

	message = {'Thongbao':'Thành công'}
	return Response(message,status=status.HTTP_200_OK)

