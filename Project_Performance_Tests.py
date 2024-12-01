import requests
# import pytest
# import pytest_randomly
import time
import numpy as np

BASE_URL = BASE_URL = "http://localhost:4567/"

BASE_Project_URL = "http://localhost:4567/projects"

#clear all items in the database, tearDown method validated - it works
def tearDown():
    response = requests.get(BASE_Project_URL)
    list_of_ids = []
    for project in response.json()["projects"]:
        list_of_ids.append(project['id'])
    i = 0
    for id in list_of_ids:
        print(f"deleting {i}")
        i+=1
        url = "http://localhost:4567/projects/{id}"
        response = requests.delete(url.format(id = id))


#method to create a certain number of projects
#n is the number of projects to create
def create_n_projects(n: int):
    timeStamp = np.zeros(n)
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    
    start_time = time.time()
    for i in range(n):
        print(i)
        #generate the random data title does not even need to be present to create a project
        data = {}
        #create the random data (post)
        response = requests.post(BASE_Project_URL, json = data)
        end_time = time.time()
        timeStamp[i] = end_time - start_time
        if response.status_code != 201: 
            raise ValueError(f"Status code not 201, {response.status_code}")
    tearDown()
    return timeStamp

#method to delete a certain number of projects
def delete_n_projects(n: int):
    timeStamp = np.zeros(n)
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    
    #First need to create those n projects
    for i in range(n):
        print(i)
        data = {}
        response = requests.post(BASE_Project_URL, json = data)
        if response.status_code != 201: 
            raise ValueError(f"Status code not 201, {response.status_code}")
    #Delete all projects 
    response = requests.get(BASE_Project_URL)
    list_of_ids = []
    for project in response.json()["projects"]:
        list_of_ids.append(project['id']) 
    start_time = time.time()
    url = "http://localhost:4567/projects/{id}"
    i = 0
    for id in list_of_ids:
        response = requests.delete(url.format(id = id))
        end_time = time.time()
        timeStamp[i] = end_time - start_time
        i+=1
    tearDown()
    return timeStamp

#method for changing a certain number of projects
def change_n_projects(n: int):
    timeStamp = np.zeros(n)
    if not isinstance(n, int):
        raise ValueError("n must be an integer")

    #timestamp how long it takes to change an object in each iteration...
    for i in range(n):
        data = {}
        response = requests.post(BASE_Project_URL, json = data)
        #j = i+1
        print(i)
        #create i projects
        # for k in range(j): #OH NO A DOUBLE FOR LOOP
        #     data = {}
        #     response = requests.post(BASE_Project_URL, json = data)

        #Get the id for one of the projects that you will change
        response = requests.get(BASE_Project_URL)
        list_of_ids = []
        for project in response.json()["projects"]:
            list_of_ids.append(project['id'])
        id_to_look_for = list_of_ids[i]
        #change 1 project out of i projects
        url = "http://localhost:4567/projects/{id}"
        data = {"title": "1"}
        time_start = time.time()
        response = requests.post(url.format(id = id_to_look_for), json = data)
        time_end = time.time()
        timeStamp[i] = time_end - time_start

    tearDown()
    return timeStamp



#Result computing
creating = create_n_projects(1000)
deleting = delete_n_projects(1000)
changing = change_n_projects(1000)

#Reporting findings
with open('output.txt', 'w') as f:
    # Write each item in the list on a new line
    f.write("Creating Projects time Marks\n")
    for item in creating:
        f.write(f"{item}\n")
    f.write("Deleting Projects time Marks\n")
    for item in deleting: 
        f.write(f"{item}\n")
    f.write("Changing Projects time Marks\n")
    for item in changing: 
        f.write(f"{item}\n")
