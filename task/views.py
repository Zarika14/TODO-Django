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
    
    
    


def get_particular_task_details(request, id) : 
    try :
        if request.method != 'GET' :
            raise Exception(f'{request.method} Method not allowed')
        
        
        if not Task.objects.filter(id = id).exists() :
            raise Exception('task not found')
        
        task = Task.objects.get(id = id)
        data = model_to_dict(task)
        
        data['created_at'] = task.created_at
        data['updated_at'] = task.updated_at
            
        return JsonResponse({'message' : data}, status = 200)

    
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = 400)
    

def update_task(request, id):
    try:
    
        if request.method != 'PUT':
            raise Exception(f'{request.method},method not allowed')
        
        if not Task.objects.filter(id = id).exists():
            raise Exception("Task not found")
        
        if not request.body :
            raise Exception('request body not found')
        
        data = json.loads(request.body)
   
   
        title = data.get('title')
        description = data.get('description')
        status = data.get('status', False)
        
        
        task = Task.objects.get(id = id)
        
        if title :
            task.title = title
        
        if description :
            task.description = description
        
        if status != None :
            status = status
        
        task.save()
        
        data = model_to_dict(task)
        
        return JsonResponse({'message' : data}, status = 200)
        
        
        
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = 400)
    
def delete_task(request,id):
    try:
        if request.method != 'DELETE':
            raise Exception(f'{request.method}, Method not allowed')
        
        if not Task.objects.filter(id = id).exists():
            raise Exception('Task does not exist')
        
        task = Task.objects.get(id = id)
        task.delete()
        
        return JsonResponse({'message': "Task deleted Successfuly"},status = 200)
        
    
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = 400)    


def list_all_task(request):

    try:
        
        if request.method != 'GET':
            raise Exception(f'{request.method}, Method not allowed')
        
        tasks = Task.objects.all()
        
        data = []
        
        for task in tasks:
            data.append(model_to_dict(task))
        
        # data = [model_to_dict(task) for task in tasks]
        
        return JsonResponse({'message ': data}, status = 200)
    
    except Exception as e:
        
        return JsonResponse({'message' : str(e)}, status = 400)  
        
        
                
                
                
                