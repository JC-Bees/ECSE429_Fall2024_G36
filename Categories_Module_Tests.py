import requests

# Run Tests using "pytest Categories_Module_Tests.py" In terminal

"""
This endpoint can be filtered with fields as URL Query Parameters.

e.g. http://localhost:4567/categories?title=eprehenderit%20in%20volu

GET /categories
return all the instances of category
HEAD /categories
headers for all the instances of category
POST /categories
we should be able to create category without a ID using the field values in the body of the message
/categories/:id
e.g. http://localhost:4567/categories/:id

GET /categories/:id
return a specific instances of category using a id
HEAD /categories/:id
headers for a specific instances of category using a id
POST /categories/:id
amend a specific instances of category using a id with a body containing the fields to amend
PUT /categories/:id
amend a specific instances of category using a id with a body containing the fields to amend
DELETE /categories/:id
delete a specific instances of category using a id
/categories/:id/todos
e.g. http://localhost:4567/categories/:id/todos

GET /categories/:id/todos
return all the todo items related to category, with given id, by the relationship named todos
HEAD /categories/:id/todos
headers for the todo items related to category, with given id, by the relationship named todos
POST /categories/:id/todos
create an instance of a relationship named todos between category instance :id and the todo instance represented by the id in the body of the message
/categories/:id/todos/:id
e.g. http://localhost:4567/categories/:id/todos/:id

DELETE /categories/:id/todos/:id
delete the instance of the relationship named todos between category and todo using the :id
/categories/:id/projects
e.g. http://localhost:4567/categories/:id/projects

GET /categories/:id/projects
return all the project items related to category, with given id, by the relationship named projects
HEAD /categories/:id/projects
headers for the project items related to category, with given id, by the relationship named projects
POST /categories/:id/projects
create an instance of a relationship named projects between category instance :id and the project instance represented by the id in the body of the message
/categories/:id/projects/:id
e.g. http://localhost:4567/categories/:id/projects/:id

DELETE /categories/:id/projects/:id
delete the instance of the relationship named projects between category and project using the :id
"""
# Base URL for the API
BASE_URL = "http://localhost:4567/categories"

# ACTUAL BEHAVIOUR WORKING

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
    url = "http://localhost:4567/categories"  
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    #data = response.json()
    #assert 'id' in data
    #assert 'title' in data
    #assert 'description' in data

# Post to todo page contents will all inputs
def test_post_data_Success():
        url = "http://localhost:4567/categories"  

        data = {
                "title": "Groceries",
                "description": "grocery lists"
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()

        assert data['id']
        assert data['title'] == "Groceries"
        assert data['description'] == "grocery lists"

# Post to todo page contents with id, fail
def test_post_data_FailID():
        url = "http://localhost:4567/categories"  

        data = {
                "id" : "4",
                "title": "Groceries",
                "description": "grocery lists"
                }

        response = requests.post(url, data)

        assert response.status_code == 415

# Test to get a category by id
def test_get_category_by_id():
    #create a test category
    data = {
                "title": "Soccer",
                "description": "to-do lists about soccer"
                }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    response = requests.get(f"{BASE_URL}/{category_id}")

    assert response.status_code == 200
    data = response.json()
    
    assert data['categories'][0]['id'] == category_id
    assert data['categories'][0]['title'] == "Soccer"
    assert data['categories'][0]['description'] == "to-do lists about soccer"

# Test to get a category by invalid id, fail
def test_get_category_by_invalid_id():
    response = requests.get(f"{BASE_URL}/100000000000000") 
    assert response.status_code == 404

# Test to update a category by id
def put_category_by_id():
    data = {
                "title": "Soccer",
                "description": "to-do lists about soccer"
                }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    updated_category_data = {
                            "title": "Soccer!!",
                            "description": "to-do lists about soccer stuff"
                            }

    response = requests.put(f"{BASE_URL}/{category_id}", json=updated_category_data)

    assert response.status_code == 200
    updated_category = response.json()
    assert updated_category['title'] == "Soccer!!"
    assert updated_category['description'] == "to-do lists about soccer stuff"

# Test to delete a category by ID
def put_category_by_id():
    data = {
                "title": "Soccer",
                "description": "to-do lists about soccer"
                }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    response = requests.delete(f"{BASE_URL}/{category_id}")

    # try to get the deleted category and make sure does not exist
    response = requests.get(f"{BASE_URL}/{category_id}")
    assert response.status_code == 404 

# Test get todos for a specific category
def test_get_todos_by_category_id():
    data = {
            "title": "Groceries",
            "description": "grocery lists"
            }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    response = requests.get(f"{BASE_URL}/{category_id}/todos")

    assert response.status_code == 200
    assert isinstance(response.json()['todos'], list)
    
# Test create todos for a specific category
def test_post_todos_by_category_id():
    data = {
            "title": "Groceries",
            "description": "grocery lists"
            }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    todo_data = {
            "title": "Apples",
            "description": "2 gala, 1 delicious"
            }

    response = requests.post(f"{BASE_URL}/{category_id}/todos", json = todo_data)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data
    assert data["title"] == "Apples"
    assert data["description"] == "2 gala, 1 delicious"

# Test update todos for a specific category: API NOT IMPLEMENTED YET

# Test delete todo by id for a specific category
def test_delete_todo_by_id_from_category():
    data = {
            "title": "Groceries",
            "description": "grocery lists"
            }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    todo_data = {
            "title": "Apples",
            "description": "2 gala, 1 delicious"
            }

    todo_response = requests.post(f"{BASE_URL}/{category_id}/todos", json = todo_data)
    todo = todo_response.json()
    todo_id = todo['id']

    response = requests.delete(f"{BASE_URL}/{category_id}/todos/{todo_id}")
    assert response.status_code == 200

    # Try to get todo and make sure it is not there
    response = requests.get(f"{BASE_URL}/{category_id}/todos/{todo_id}")
    assert response.status_code == 404
     
# Test get projects for a specific category
def test_get_projects_by_category_id():
    data = {
            "title": "Groceries",
            "description": "grocery lists"
            }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    response = requests.get(f"{BASE_URL}/{category_id}/projects")

    assert response.status_code == 200
    assert isinstance(response.json()['projects'], list)
    
# Test create projects for a specific category
def test_post_projects_by_category_id():
    data = {
            "title": "Groceries",
            "description": "grocery lists"
            }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    project_data = {
            "title": "Project 1",
            }

    response = requests.post(f"{BASE_URL}/{category_id}/projects", json = project_data)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data
    assert data["title"] == "Project 1"

# Test update projects for a specific category: API NOT IMPLEMENTED YET

# Test delete project by id for a specific category
def test_delete_todo_by_id_from_category():
    data = {
            "title": "Groceries",
            "description": "grocery lists"
            }
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category['id']

    project_data = {
            "title": "Project 1",
            }

    project_response = requests.post(f"{BASE_URL}/{category_id}/projects", json = project_data)
    project = project_response.json()
    project_id = project['id']

    response = requests.delete(f"{BASE_URL}/{category_id}/projects/{project_id}")
    assert response.status_code == 200

    # Try to get project and make sure it is not there
    response = requests.get(f"{BASE_URL}/{category_id}/projects/{project_id}")
    assert response.status_code == 404
     
# WHEN EXPECTED BEHAVIOUR FAILS
