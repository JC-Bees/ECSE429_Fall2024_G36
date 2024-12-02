import requests
import pytest
import numpy as np
import time

# Run Tests using "pytest Todo_Module_Tests.py" In terminal

BASE_URL = "http://localhost:4567/"

BASE_URL_POST = "http://localhost:4567/todos"

timeCurr = time.time()

TestNum = 1000

@pytest.fixture(autouse=True)
def tearDown():
    # This function will run before each test to reset all variables
        yield
        url = BASE_URL+"todos"
        response = requests.get(url)
        if response.status_code == 200:
                # if there are todos in the system
                todos = response.json().get("todos", [])
                for todo in todos:
                        id = todo["id"]
                        requests.delete(f"{url}/{id}") # deletes each todo in system
        url = "http://localhost:4567/categories"
        response = requests.get(url)
        if response.status_code == 200:
                # if there are projects in the system
                categories = response.json().get("categories", [])
                for category in categories:
                        id = category["id"]
                        requests.delete(f"{url}/{id}") # deletes each project in system
        


# Post to todo page contents will all inputs | CREATE OBJECT OPERATION EXPERIMENT
def test_todo_post_data_Success_FullBody():
        url = BASE_URL + "todos"  
        PostTimes = np.zeros(TestNum)
        for i in range(TestNum):
                
                dataPOST = {
                "title": f"titletest{i}",
                "doneStatus": False,
                "description": f"descriptiontest{i}"
                }
                start = time.perf_counter()
                response = requests.post(url, json = dataPOST)
                end = time.perf_counter()
                assert response.status_code == 201
                PostTimes[i] = end - start

        np.savetxt(f"PostTimes_{timeCurr}.csv", PostTimes, delimiter=",")
        


# Put todo/id test with full body | CHANGE OBJECT OPERATION EXPERIMENT
def test_todo_id_put_Success_full():
        url = BASE_URL + "todos/{id}"  
        
        PutTimes = np.zeros(TestNum)
        for i in range(TestNum):

                #Setup
                dataPOST = {
                "title": f"titletest{i}",
                "doneStatus": False,
                "description": f"descriptiontest{i}"
                }
                response = requests.post(BASE_URL_POST, json = dataPOST)# Worsens the CPU and RAM Results
                ID = response.json()['id']

                dataPUT = {
                        "title": f"titletestjcb{i}",
                        "doneStatus": True,
                        "description": f"descriptiontestjcb{i}"
                        }
                start = time.perf_counter()
                response = requests.put(url.format(id = ID), json = dataPUT)
                end = time.perf_counter()
                assert response.status_code == 200
                PutTimes[i] = end - start

        np.savetxt(f"PutTimes_{timeCurr}.csv", PutTimes, delimiter=",")
        



# Succesffuly create, then delete, then check for an id | DELETE OBJECT OPERATION EXPERIMENT
def test_todo_id_delete():
        url = BASE_URL + "todos/{id}"    
        DeleteTimes = np.zeros(TestNum)
        for i in range(TestNum):

                #Setup
                dataPOST = {
                "title": f"titletest{i}",
                "doneStatus": False,
                "description": f"descriptiontest{i}"
                }
                response = requests.post(BASE_URL_POST, json = dataPOST) # Worsens the CPU and RAM Results
                response = requests.post(BASE_URL_POST, json = dataPOST) # Worsens the CPU and RAM Results
                ID = response.json()['id']

                start = time.perf_counter()
                response = requests.delete(url.format(id = ID))
                end = time.perf_counter()
                assert response.status_code == 200

                DeleteTimes[i] = end - start
        np.savetxt(f"DeleteTimes_{timeCurr}.csv", DeleteTimes, delimiter=",")






