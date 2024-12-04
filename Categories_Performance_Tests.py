import requests
import pytest
import numpy as np
import time

# Run Tests using "pytest Categories_Performance_Tests.py" In terminal

BASE_URL = "http://localhost:4567/"

timeCurr = time.time()

TestNum = 1000

@pytest.fixture(autouse=True)
def tearDown():
    # This function will run before each test to reset all variables
    yield
    response = requests.get(BASE_URL + "categories")
    if response.status_code == 200:
        # if there are categories in the system
        categories = response.json().get("categories", [])
        for category in categories:
            id = category["id"]
            requests.delete(f"{BASE_URL}/{id}") # deletes each category in system       


# Post to categories page contents will all inputs | CREATE OBJECT OPERATION EXPERIMENT
def test_categories_post_data_Success_FullBody():
        url = BASE_URL + "categories"  
        PostTimes = np.zeros(TestNum)
        for i in range(TestNum):
                
                dataPOST = {
                "title": f"titletest{i}",
                "description": f"descriptiontest{i}"
                }
                start = time.perf_counter()
                response = requests.post(url, json = dataPOST)
                end = time.perf_counter()
                assert response.status_code == 201
                PostTimes[i] = end - start

        np.savetxt(f"PostTimes_Categories_{timeCurr}.csv", PostTimes, delimiter=",")
        


# Put categories/id test with full body | CHANGE OBJECT OPERATION EXPERIMENT
def test_categories_id_put_Success_full():
        url = BASE_URL + "categories/{id}"  
        
        PutTimes = np.zeros(TestNum)
        for i in range(TestNum):

                #Setup
                dataPOST = {
                "title": f"titletest{i}",
                "description": f"descriptiontest{i}"
                }
                response = requests.post(BASE_URL + "categories", json = dataPOST)# Worsens the CPU and RAM Results
                ID = response.json()['id']

                dataPUT = {
                        "title": f"titletest_new{i}",
                        "description": f"descriptiontest_new{i}"
                        }
                start = time.perf_counter()
                response = requests.put(url.format(id = ID), json = dataPUT)
                end = time.perf_counter()
                assert response.status_code == 200
                PutTimes[i] = end - start

        np.savetxt(f"PutTimes_Categories_{timeCurr}.csv", PutTimes, delimiter=",")
        


# Succesffuly create, then delete, then check for an id | DELETE OBJECT OPERATION EXPERIMENT
def test_categories_id_delete():
        url = BASE_URL + "categories/{id}"    
        DeleteTimes = np.zeros(TestNum)
        for i in range(TestNum):

                #Setup
                dataPOST = {
                "title": f"titletest{i}",
                "description": f"descriptiontest{i}"
                }
                response = requests.post(BASE_URL + "categories", json = dataPOST) # Worsens the CPU and RAM Results
                response = requests.post(BASE_URL + "categories", json = dataPOST) # Worsens the CPU and RAM Results
                ID = response.json()['id']

                start = time.perf_counter()
                response = requests.delete(url.format(id = ID))
                end = time.perf_counter()
                assert response.status_code == 200

                DeleteTimes[i] = end - start
        np.savetxt(f"DeleteTimes_Categories_{timeCurr}.csv", DeleteTimes, delimiter=",")


