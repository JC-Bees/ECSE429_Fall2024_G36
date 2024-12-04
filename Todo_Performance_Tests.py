import requests
import pytest
import numpy as np
import time
import psutil
import os

# Run Tests using "pytest Todo_Module_Tests.py" In terminal

BASE_URL = "http://localhost:4567/"

BASE_URL_POST = "http://localhost:4567/todos"

timeCurr = time.time()
process = psutil.Process(os.getpid())
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
        PostData = np.zeros((TestNum,3))
        for i in range(TestNum):
                
                dataPOST = {
                "title": f"titletest{i}",
                "doneStatus": False,
                "description": f"descriptiontest{i}"
                }
                start = time.perf_counter()
                psutil.cpu_percent(0.0)
                response = requests.post(url, json = dataPOST)
                PostData[i,1] = psutil.cpu_percent(0.1)
                PostData[i,2] = (psutil.virtual_memory().available / psutil.virtual_memory().total)* 100
                end = time.perf_counter()
                assert response.status_code == 201
                PostData[i,0] = end - start

        np.savetxt(f"PostData_Todo_{timeCurr}.csv", PostData, delimiter=",")

        


# Put todo/id test with full body | CHANGE OBJECT OPERATION EXPERIMENT
def test_todo_id_put_Success_full():
        url = BASE_URL + "todos/{id}"  
        
        PutData = np.zeros((TestNum,3))
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
                PutData[i,1] = psutil.cpu_percent(0.1)
                PutData[i,2] = (psutil.virtual_memory().available / psutil.virtual_memory().total)* 100
                end = time.perf_counter()
                assert response.status_code == 200
                PutData[i,0] = end - start

        np.savetxt(f"PutData_Todo_{timeCurr}.csv", PutData, delimiter=",")
        



# Succesffuly create, then delete, then check for an id | DELETE OBJECT OPERATION EXPERIMENT
def test_todo_id_delete():
        url = BASE_URL + "todos/{id}"    
        DeleteData = np.zeros((TestNum,3))
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
                DeleteData[i,1] = psutil.cpu_percent(0.1)
                DeleteData[i,2] = (psutil.virtual_memory().available / psutil.virtual_memory().total)* 100
                end = time.perf_counter()
                assert response.status_code == 200

                DeleteData[i,0] = end - start
        np.savetxt(f"DeleteData_Todo_{timeCurr}.csv", DeleteData, delimiter=",")






