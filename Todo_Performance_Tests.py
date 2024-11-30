import requests
import pytest
import pytest_randomly

# Run Tests using "pytest Todo_Module_Tests.py" In terminal

BASE_URL = BASE_URL = "http://localhost:4567/"

BASE_URL_POST = "http://localhost:4567/todos"

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


# Get the todo page contents
def test_todo_get_data():
    url = BASE_URL + "todos"  

    #Setup
    data = {"title": "StandardTitle1","doneStatus" : False, "description":"StandardDescription1"}
    response = requests.post(BASE_URL_POST, json = data)
    assert response.status_code == 201
    
    data = {"title": "StandardTitle2","doneStatus" : False, "description":"StandardDescription2"}
    response = requests.post(BASE_URL_POST, json = data)
    assert response.status_code == 201

    #Test
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()['todos']
    
    assert 'id' in data[0]
    assert 'title' in data[0]
    assert 'doneStatus' in data[0]
    assert 'description' in data[0]


# Post to todo page contents will all inputs | CREATE OBJECT OPERATION
def test_todo_post_data_Success_FullBody():
        url = BASE_URL + "todos"  

        data = {
                "title": "titletest",
                "doneStatus": False,
                "description": "descriptiontest"
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == 'titletest'
        assert data['doneStatus'] == 'false'
        assert data['description'] == "descriptiontest"

"""
# Post to todo page contents will all inputs
def test_todo_id_post_data_Success_FullBody():
        url = BASE_URL + "todos/{id}"  

        #Setup
        data = {"title": "StandardTitle1","doneStatus" : False, "description":"StandardDescription1"}
        response = requests.post(BASE_URL_POST, json = data)
        assert response.status_code == 201
        
        data = {"title": "StandardTitle2","doneStatus" : False, "description":"StandardDescription2"}
        response = requests.post(BASE_URL_POST, json = data)
        assert response.status_code == 201

        ID = response.json()['id']

        data = {
                "title": "titletestjcb",
                "doneStatus": False,
                "description": "descriptiontestjcb"
                }

        response = requests.post(url.format(id = ID), json = data)

        assert response.status_code == 200

        data = response.json()
        assert data['title'] == 'titletestjcb'
        assert data['doneStatus'] == 'false'
        assert data['description'] == "descriptiontestjcb"
"""

# Put todo/id test with full body | CHANGE OBJECT OPERATION
def test_todo_id_put_Success_full():
        url = BASE_URL + "todos/{id}"  

        #Setup
        data = {"title": "StandardTitle1","doneStatus" : False, "description":"StandardDescription1"}
        response = requests.post(BASE_URL_POST, json = data)
        assert response.status_code == 201
        
        data = {"title": "StandardTitle2","doneStatus" : False, "description":"StandardDescription2"}
        response = requests.post(BASE_URL_POST, json = data)
        assert response.status_code == 201

        ID = response.json()['id']
        data = {
                "id" : 1,
                "title": "titletestjcb",
                "doneStatus": False,
                "description": "descriptiontestjcb"
                }

        response = requests.put(url.format(id = ID), json = data)

        assert response.status_code == 200

        data = response.json()
        assert data['title'] == 'titletestjcb'
        assert data['doneStatus'] == 'false'
        assert data['description'] == "descriptiontestjcb"


# Succesffuly create, then delete, then check for an id | DELETE OBJECT OPERATION
def test_todo_id_delete():
        url = BASE_URL + "todos/{id}"    

        data ={"title":"deleteTest"}

        response = requests.post(BASE_URL_POST,json = data)

        data = response.json()

        ID = data['id']

        assert data['title'] == "deleteTest"

        response = requests.delete(url.format(id = ID))

        assert response.status_code == 200

        response = requests.get(url.format(id = ID))

        assert response.status_code == 404







