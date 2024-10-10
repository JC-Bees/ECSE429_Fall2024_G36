import requests
import pytest

# Run Tests using "pytest Projects_Module_Tests.py" In terminal

BASE_URL = "http://localhost:4567/"

@pytest.fixture(autouse=True)
def tearDown():
    # This function will run before each test to reset all variables
    yield
    url = "http://localhost:4567/projects"
    response = requests.get(url)
    if response.status_code == 200:
        # if there are projects in the system
        projects = response.json().get("projects", [])
        for project in projects:
            id = project["id"]
            requests.delete(f"{url}/{id}") # deletes each project in system

#create project for every test
def create_project():
    url = "http://localhost:4567/projects"

    data = {
        "title": "Testing Project"
    }
    response = requests.post(url, json = data)

    response = requests.get(BASE_URL + "projects")

    id = response.json()["projects"][0]['id']
    return id

def create_taskof():
    url = "http://localhost:4567/todos"

    data = {
        "title": "finish this project"
    }
    response = requests.post(url, json = data)

    response = requests.get(url)

    print("is this is?")
    print(response.json())
    id = response.json()["todos"][0]['id']
    return id

# First general test to make sure everything works 
def test_todo_get_GUI():
    url = BASE_URL + "gui/entities"  # Adjust the port if needed
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'text/html'

#/projects
# Make sure that all fields are available when getting all projects
def test_projects_get_data():
    id = create_project()
    url = BASE_URL + "projects"  
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()['projects']
    assert 'id' in data[0]
    assert 'title' in data[0]
    assert 'active' in data[0]
    assert 'completed' in data[0]
    assert 'description' in data[0]

# Get Head information for project
def test_projects_head_data():
    url = BASE_URL + "projects"  
    response = requests.head(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

# Post to Project page contents with all inputs
def test_projects_post_data_Success_FullBody():
        url = BASE_URL + "projects"  

        data = {
                "title": "titletest",
                "completed": False,
                "active": True,
                "description": "this is a test"
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == 'titletest'
        assert data['completed'] == 'false'
        assert data['active'] == "true"
        assert data['description'] == "this is a test"

# Post to Project page contents with title only
def test_projects_post_data_Success_TitleOnly():
        url = BASE_URL + "projects"  

        data = {
                "title": "titletest",
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == 'titletest'
        assert data['completed'] == 'false'
        assert data['active'] == "false"
        assert data['description'] == ""

#Create a project without any fields
def test_projects_post_data_Success_NoFields():
        url = BASE_URL + "projects"  

        data = {
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == ''
        assert data['completed'] == 'false'
        assert data['active'] == "false"
        assert data['description'] == ""

#Undocumented put method testing for /project
def test_projects_undocumented_put_method():
        url = BASE_URL + "projects"  

        response = requests.put(url)

        assert response.status_code == 405  

#Undocumented delete method testing for /project
def test_projects_undocumented_delete_method():
        url = BASE_URL + "projects"  

        response = requests.delete(url)

        assert response.status_code == 405 

#Undocumented options method testing for /project
def test_projects_undocumented_options_method_fail_test():
        url = BASE_URL + "projects"  

        response = requests.options(url)

        assert response.status_code == 405 

#Undocumented patch method testing for /project
def test_projects_undocumented_patch_method():
        url = BASE_URL + "projects"  

        response = requests.patch(url)

        assert response.status_code == 405

#Get a project with a specific id
def test_project_id_get_data():
    id = create_project()


    url = BASE_URL + "projects/{id}"  
    response = requests.get(url.format(id=id))

    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()['projects']

    data = data[0]
    data["id"] = "1"
    data["title"] = "Office Work"
    data["completed"] = 'false'
    data["active"] = 'fasle'
    data['description'] = ''

#Get a project with a wrong id
def test_project_wrong_id_get_data():
    url = BASE_URL + "projects/{id}"  
    
    response = requests.get(url.format(id = 1000))

    # Check that the response status code is 200 OK
    assert response.status_code == 404

    assert response.json() == {"errorMessages":["Could not find an instance with projects/1000"]}

#Get a project with no id (test will fail) 
def test_project_no_id_fail_test():
    url = BASE_URL + "projects/{id}"  
    
    response = requests.get(url)

    # Check that the response status code is 200 OK
    assert response.status_code == 400

# Get Head information for project with body input
def test_project_id_head_data_body():
    id = create_project()
    url = BASE_URL + "projects/{id}"  

    response = requests.head(url.format(id = id))
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

#Test if Put updates the informtion on a project
def test_project_put_method():
    id = create_project()
    url = BASE_URL + "projects/{id}"  

    data = {
                "title": "finish the coffee",
                }

    response = requests.put(url.format(id = id), json = data)

    assert response.status_code == 200

    data1 = response.json()
    response = requests.get(url.format(id = id))
    data2 = response.json()['projects'][0]

    assert data1['title'] == data2['title']
    assert data1['active'] == data2['active']
    assert data1['completed'] == data2['completed']
    assert data1['description'] == data2['description']

#Post test to change title with given id
def test_project_post_method():
    id = create_project()
    url = BASE_URL + "projects/{id}"  

    data = {
                "title": "finish the coffee",
                }

    response = requests.post(url.format(id = id), json = data)

    assert response.status_code == 200

    data1 = response.json()
    response = requests.get(url.format(id = id))
    data2 = response.json()['projects'][0]

    assert data1['title'] == data2['title']
    assert data1['active'] == data2['active']
    assert data1['completed'] == data2['completed']
    assert data1['description'] == data2['description']

#Undocumented method
def test_project_post_fail_method():
    url = BASE_URL + "projects/{id}"  

    data = {
                "title": "finish the coffee",
                }

    response = requests.put(url, json = data)

    assert response.status_code == 400

#delete a project with its id
def test_delete_project_test(): 
    id = create_project()
    url = BASE_URL + "projects/{id}"
    

    response = requests.delete(url.format(id = id))

    assert response.status_code == 200
    response = requests.get(url.format(id = id))

    assert response.status_code == 404

#make sure the method is undocumented
def test_projects_id_options_method_fail_test():
    url = BASE_URL + "projects/{id}"  

    data = {
                "title": "finish the coffee",
                }

    response = requests.options(url, json = data)

    assert response.status_code == 405

#make sure the method is undocumented
def test_projects_id_patch_method_fail_test():
    url = BASE_URL + "projects/{id}"  

    data = {
                "title": "finish the coffee",
                }

    response = requests.patch(url, json = data)

    assert response.status_code == 405

#make sure I can get all the categories related to a project
def test_projects_id_categories_id():
    url = BASE_URL + "projects/{id}/categories"

    response = requests.get(url.format(id=1))

    assert response.status_code == 200

#Succesfully get the head info for categories of a specific project
def test_project_id_categories_head():
    url = BASE_URL + "projects/:id/categories"  
    response = requests.head(url.format(id=1))
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

#Successfully post a category to a specific project
def test_project_id_categories_post():
    id = create_project()
    url = BASE_URL + "projects/{id}/categories"

    data = {
        "id": "1"
    }

    response = requests.post(url.format(id=id), json = data)
    print("look here")
    assert response.status_code == 201
    response = requests.get(url.format(id=id))
    
    data = response.json()
    test = False
    for category in data['categories']:
        if category['id'] == '1': 
            assert True
            test = True
    if not test:
        assert False

#Undocumented method Put
def test_project_id_categories_put_method():
    url = BASE_URL + "projects/{id}/categories"

    data = {
        "id": "1"
    }

    response = requests.put(url.format(id=1), json = data)

    assert response.status_code == 405

#Undocumented Delete method
def test_project_id_categories_delete_method():
    url = BASE_URL + "projects/{id}/categories"

    data = {
        "id": "1"
    }

    response = requests.delete(url.format(id=1), json = data)

    assert response.status_code == 405

#Undocumented options method, should return 405 but returns 200
def test_project_id_categories_options_fail_method():
    url = BASE_URL + "projects/{id}/categories"

    data = {
        "id": "1"
    }

    response = requests.options(url.format(id=1), json = data)

    assert response.status_code == 405

#undocumented Patch method
def test_project_id_categories_patch_method():
    url = BASE_URL + "projects/{id}/categories"

    data = {
        "id": "1"
    }

    response = requests.patch(url.format(id=1), json = data)

    assert response.status_code == 405

#Succesful Deletion of a categorie and project relationship
def test_project_id_categories_delete_method1():
    id = create_project()
    #first create the relation betwen the category and ID
    url = BASE_URL + "projects/{id}/categories"

    #relating the category with ID = 1
    data = {
        "id": "1"
    }

    response = requests.post(url.format(id=id), json = data)

    assert response.status_code == 201

    url1 = BASE_URL + "projects/{id}/categories/1"

    response = requests.delete(url1.format(id = id))

    assert response.status_code == 200

#Seccesfully catch trying to delete a category relationship when there is no such category to the oriject
def test_project_id_categories_delete_catch_error():
    url1 = BASE_URL + "projects/1/categories/10000"

    response = requests.delete(url1)

    assert response.status_code == 404

    assert response.json() == {"errorMessages":["Could not find any instances with projects/1/categories/10000"]} 

#Get undocumented method, should return a 405 status
def test_porject_id_category_id_get_method_fail():
    url1 = BASE_URL + "projects/1/categories/1"

    response = requests.get(url1)

    assert response.status_code == 405

#Undocumented Put method
def test_project_id_category_id_put_method_fail():
    url1 = BASE_URL + "projects/1/categories/1"

    response = requests.put(url1)

    assert response.status_code == 405

#undocumented Post method, should return 405 but does not
def test_project_id_category_id_post_method_fail():
    url1 = BASE_URL + "projects/1/categories/1"

    response = requests.post(url1)

    assert response.status_code == 405

#undocumented options method, should return 405 but does not
def test_project_id_category_id_options_method_fail():
    url1 = BASE_URL + "projects/1/categories/1"

    response = requests.options(url1)

    assert response.status_code == 405

#undocumented head method, should return 405 but does not
def test_project_id_category_id_head_method_fail():
    url1 = BASE_URL + "projects/1/categories/1"

    response = requests.head(url1)

    assert response.status_code == 405

#undocumented patch method, should return 405 
def test_project_id_category_id_patch_method_fail():
    url1 = BASE_URL + "projects/1/categories/1"

    response = requests.patch(url1)

    assert response.status_code == 405

#Post Method to add a task to a project
def test_project_id_task():
    id = create_project()
    id_task = create_taskof()
    url = BASE_URL + "projects/{id}/tasks"

    data = {
        "id" : f"{id_task}"
    }

    response = requests.post(url.format(id = id), json = data)

    assert response.status_code == 201

#Head method testing for task to project
def test_projet_id_tasks_head_method():
    url = BASE_URL + "projects/1/tasks"  # Adjust the port if needed
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

#Get method for a tasks for a specific project
def test_project_id_tasks_get_method():
    id = create_project()
    id_task = create_taskof()
    #link tasks to the specific project
    url = BASE_URL + "projects/{id}/tasks"

    data = {
        "id" : f"{id_task}"
    }

    response = requests.post(url.format(id = id), json = data)

    assert response.status_code == 201

    #get that specific task

    response = requests.get(url.format(id = id))

    stop = False
    for field in response.json()['todos']:
        if field["id"] == f"{id_task}":
            stop = True
    if not stop:
        assert False
    
    assert response.status_code == 200

#Undocumented Put method for tasks of a project
def test_project_id_tasks_put_method():
    url = BASE_URL + "projects/1/tasks"

    response = requests.put(url)

    assert response.status_code == 405

#undocumented delete method
def test_project_id_tasks_delete_method():
    url = BASE_URL + "projects/1/tasks"

    response = requests.delete(url)

    assert response.status_code == 405

#undocumented options method
def test_project_id_tasks_options_fail_method():
    url = BASE_URL + "projects/1/tasks"

    response = requests.options(url)

    assert response.status_code == 405

#undocumented patch method
def test_project_id_tasks_patch_method():
    url = BASE_URL + "projects/1/tasks"

    response = requests.patch(url)

    assert response.status_code == 405

#delete a task connected to a project
def test_project_id_task_id_methiod():
    id = create_project()
    id_task = create_taskof()
    url = "http://localhost:4567/projects/{id}/tasks"


    data = {
        "id": f"{id_task}"
    }

    response = requests.post(url.format(id = id), json = data)

    assert response.status_code == 201

    url = "http://localhost:4567/projects/{id}/tasks/{id_2}"
    response = requests.delete(url.format(id = id, id_2 = id_task))

    assert response.status_code == 200

#undocumented get method 
def test_project_id_taks_id_get_fail_method1():
    url = "http://localhost:4567/projects/3/tasks"


    data = {
        "id": "2"
    }

    response = requests.get(url, json = data)

    assert response.status_code == 405

#undocumented put method 
def test_project_id_taks_id_put_method1():
    url = "http://localhost:4567/projects/3/tasks"


    data = {
        "id": "2"
    }

    response = requests.put(url, json = data)

    assert response.status_code == 405

#undocumented post method 
def test_project_id_taks_id_post_fail_method1():
    url = "http://localhost:4567/projects/3/tasks"


    data = {
        "id": "2"
    }

    response = requests.post(url, json = data)

    assert response.status_code == 405

#undocumented options method 
def test_project_id_taks_id_options_fail_method1():
    url = "http://localhost:4567/projects/3/tasks"


    data = {
        "id": "2"
    }

    response = requests.options(url, json = data)

    assert response.status_code == 405

#undocumented head method 
def test_project_id_taks_id_head_fail_method1():
    url = "http://localhost:4567/projects/3/tasks"


    data = {
        "id": "2"
    }

    response = requests.head(url, json = data)

    assert response.status_code == 405

#undocumented patch method 
def test_project_id_taks_id_patch_method1():
    url = "http://localhost:4567/projects/3/tasks"


    data = {
        "id": "2"
    }

    response = requests.patch(url, json = data)

    assert response.status_code == 405