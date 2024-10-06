import requests

# Run Tests using "pytest Todo_Module_Tests.py" In terminal

"""
This endpoint can be filtered with fields as URL Query Parameters.

e.g. http://localhost:4567/todos?title=nt%20mollit%20anim%20id%20es

GET /todos
return all the instances of todo
HEAD /todos
headers for all the instances of todo
POST /todos
we should be able to create todo without a ID using the field values in the body of the message
/todos/:id
e.g. http://localhost:4567/todos/:id

GET /todos/:id
return a specific instances of todo using a id
HEAD /todos/:id
headers for a specific instances of todo using a id
POST /todos/:id
amend a specific instances of todo using a id with a body containing the fields to amend
PUT /todos/:id
amend a specific instances of todo using a id with a body containing the fields to amend
DELETE /todos/:id
delete a specific instances of todo using a id
/todos/:id/categories
e.g. http://localhost:4567/todos/:id/categories

GET /todos/:id/categories
return all the category items related to todo, with given id, by the relationship named categories
HEAD /todos/:id/categories
headers for the category items related to todo, with given id, by the relationship named categories
POST /todos/:id/categories
create an instance of a relationship named categories between todo instance :id and the category instance represented by the id in the body of the message
/todos/:id/categories/:id
e.g. http://localhost:4567/todos/:id/categories/:id

DELETE /todos/:id/categories/:id
delete the instance of the relationship named categories between todo and category using the :id
/todos/:id/tasksof
e.g. http://localhost:4567/todos/:id/tasksof

GET /todos/:id/tasksof
return all the project items related to todo, with given id, by the relationship named tasksof
HEAD /todos/:id/tasksof
headers for the project items related to todo, with given id, by the relationship named tasksof
POST /todos/:id/tasksof
create an instance of a relationship named tasksof between todo instance :id and the project instance represented by the id in the body of the message
/todos/:id/tasksof/:id
e.g. http://localhost:4567/todos/:id/tasksof/:id

DELETE /todos/:id/tasksof/:id
delete the instance of the relationship named tasksof between todo and project using the :id

"""

# First general test to make sure everything works 
def test_get_GUI():
    url = "http://localhost:4567/gui/entities"  # Adjust the port if needed
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'text/html'

# Get the todo page contents
def test_get_data():
    url = "http://localhost:4567/todos"  
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()
    assert 'id' in data
    assert 'title' in data
    assert 'doneStatus' in data
    assert 'description' in data

# Post to todo page contents will all inputs
def test_post_data_Success():
        url = "http://localhost:4567/todos"  

        data = {
                "title": "titletest",
                "doneStatus": "false",
                "description": "descriptiontest"
                }

        response = requests.post(url, json = data)

        assert response.status_code == 200

        data = response.json()

        assert data['id']
        assert data['title'] == 'titletest'
        assert data['doneStatus'] == false
        assert data['description'] == "descriptiontest"

# Post to todo page contents with id, fail
def test_post_data_FailID():
        url = "http://localhost:4567/todos"  

        data = {
                "id" : "4",
                "title": "titletest",
                "doneStatus": "false",
                "description": "descriptiontest"
                }

        response = requests.post(url, data)

        assert response.status_code == 415

