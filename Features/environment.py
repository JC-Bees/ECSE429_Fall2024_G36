import requests
import behave

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