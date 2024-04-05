from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json

from task.models import Task
# Create your views here.

def create_task(request):
    try:
        if request.method != 'POST' :
            raise Exception(f'{request.method} method not allowed')
        
        if not request.body :
            raise Exception('request body not found')
        
        data = json.loads(request.body)
   
   
        title = data.get('title')
        description = data.get('description')
        status = data.get('status', False)
        
        
        if not title :
            raise Exception('Title can not be empty')
        
        
        task = Task(title = title, description = description, status = status)
        task.save()
        
    
        
        data = model_to_dict(task)
        return JsonResponse({'message' : data}, status = 200)

    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = 400 )
    
    


def get_particular_task_details(request, **kwargs) : 
    # print(id)
    return JsonResponse({}, status = 200)
    