import requests
import behave
import random

BASE_URL = 'http://localhost:4567'

#Deleting all todos before the start of each sceneraio
def before_scenario(context, scenario):
    #Get all todos
    response = requests.get(BASE_URL + '/todos')
    if response.status_code == 200:
        todo_items = response.json()['todos']
        #Iterate through them and delete
        for item in todo_items:
            id = item["id"]
            requests.delete(BASE_URL + f"/todos/{id}")
    #Get all catgories
    response = requests.get(BASE_URL + '/categories')
    if response.status_code == 200:
        todo_items = response.json()['categories']
        #Iterate through them and delete
        for item in todo_items:
            id = item["id"]
            requests.delete(BASE_URL + f"/categories/{id}") 
    #Get all projects
    response = requests.get(BASE_URL + '/projects')
    if response.status_code == 200:
        todo_items = response.json()['projects']
        #Iterate through them and delete
        for item in todo_items:
            id = item["id"]
            requests.delete(BASE_URL + f"/projects/{id}") 
