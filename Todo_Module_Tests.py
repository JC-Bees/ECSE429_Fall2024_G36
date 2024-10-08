import requests

# Run Tests using "pytest Todo_Module_Tests.py" In terminal

BASE_URL = "http://localhost:4567/"

# First general test to make sure everything works 
def test_todo_get_GUI():
    url = BASE_URL + "gui/entities"  # Adjust the port if needed
    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'text/html'

# Get the todo page contents
def test_todo_get_data():
    url = BASE_URL + "todos"  
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

    # Get the todo page contents with a body
def test_todo_get_data_body():
    url = BASE_URL + "todos"  

    data = {"id":1}

    response = requests.get(url, json = data)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()['todos']

    assert 'id' in data[0]
    assert 'title' in data[0]
    assert 'doneStatus' in data[0]
    assert 'description' in data[0]

# Get Head information for todo
def test_todo_head_data():
    url = BASE_URL + "todos"  
    response = requests.head(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    # Get Head information for todo with body input
def test_todo_head_data_body():
    url = BASE_URL + "todos"  

    data = {"id":1}
    response = requests.head(url, json = data)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'


# Post to todo page contents will all inputs
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

# Post to todo page contents will only title and doneStatus=true
def test_todo_post_data_Success_TitleandStatus():
        url = BASE_URL + "todos"  

        data = {
                "title": "titletestonly",
                "doneStatus" : True
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == 'titletestonly'
        assert data['doneStatus'] == 'true'
        
# Post to todo page contents will only title
def test_todo_post_data_Success_TitleOnly():
        url = BASE_URL + "todos"  

        data = {
                "title": "titletestonly",
                }

        response = requests.post(url, json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == 'titletestonly'

# Post to todo page contents with empty title
def test_todo_post_data_Fail_TitleEmpty():
        url = BASE_URL + "todos"  

        data = {
                "title": "",
                "doneStatus": False,
                "description": "descriptiontest"
                }

        response = requests.post(url, json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["Failed Validation: title : can not be empty"]} 

# Post to todo page contents with a specified id
def test_todo_post_data_Fail_ID():
        url = BASE_URL + "todos"  

        data = {
                "id": 1,
                "title": "",
                "doneStatus": False,
                "description": "descriptiontest"
                }

        response = requests.post(url, json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["Invalid Creation: Failed Validation: Not allowed to create with id"]} 

# Post to todo page contents with an empty body
def test_todo_post_data_Fail_EmptyBody():
        url = BASE_URL + "todos"  

        data = {  }

        response = requests.post(url, json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["title : field is mandatory"]} 

# Post to todo page contents with a bad key| Testing for malformed json body
def test_todo_post_data_Fail_BadKey():
        url = BASE_URL + "todos"  

        data = {"bobbyMcgee":"Janis Joplin" }

        response = requests.post(url, json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["Could not find field: bobbyMcgee"]} 

# patch todo test | Undocumented
def test_todo_patch():
        url = BASE_URL + "todos"  

        response = requests.patch(url)

        assert response.status_code == 405

# put todo test | Undocumented
def test_todo_put():
        url = BASE_URL + "todos"  

        response = requests.put(url)

        assert response.status_code == 405

# delete todo test | Undocumented
def test_todo_delete():
        url = BASE_URL + "todos"  

        response = requests.delete(url)

        assert response.status_code == 405

# options todo test | Undocumented
def test_todo_options():
        url = BASE_URL + "todos"  

        response = requests.options(url)

        assert response.status_code == 200

### TODOS/:ID SECTION

# Get the todo page contents by id
def test_todo_id_get_data():
    url = BASE_URL + "todos/{id}"  
    
    response = requests.get(url.format(id = 1))

    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()['todos']

    assert 'id' in data[0]
    assert 'title' in data[0]
    assert 'doneStatus' in data[0]
    assert 'description' in data[0]

# Fail to get todo data by id as no params are present
def test_todo_id_get_data_Fail_paramMissing():
    url = BASE_URL + "todos/:id"   

    response = requests.get(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 404

    assert response.json() == {"errorMessages":["Could not find an instance with todos/:id"]}
    
# Fail to get todo data by id as id is not in system
def test_todo_id_get_data_Fail_paramMissing():
    url = BASE_URL + "todos/{id}"   

    response = requests.get(url.format(id = 101) )
    
    # Check that the response status code is 200 OK
    assert response.status_code == 404

    assert response.json() == {"errorMessages":["Could not find an instance with todos/101"]} 

# Fail to get todo data by id as no params are present
def test_todo_id_get_data_Fail_paramMissing():
    url = BASE_URL + "todos/{id}"   

    response = requests.get(url.format(id = "bobby") )
    
    # Check that the response status code is 200 OK
    assert response.status_code == 404

    assert response.json() == {"errorMessages":["Could not find an instance with todos/bobby"]} 


# Fail to Get Head information for todo as no id is specified
def test_todo_id_head_data_fail():
    url = BASE_URL + "todos/:id"    
    response = requests.head(url)
    
    # Check that the response status code is 200 OK
    assert response.status_code == 404


# Get Head information for todo with body input
def test_todo_id_head_data_body():
    url = BASE_URL + "todos/{id}"  

    response = requests.head(url.format(id = 1))
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'


# Post to todo page contents will all inputs
def test_todo_id_post_data_Success_FullBody():
        url = BASE_URL + "todos/{id}"  

        data = {
                "title": "titletestjcb",
                "doneStatus": False,
                "description": "descriptiontestjcb"
                }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 200

        data = response.json()
        assert data['title'] == 'titletestjcb'
        assert data['doneStatus'] == 'false'
        assert data['description'] == "descriptiontestjcb"

# Post to todo page contents with empty body but specify id
def test_todo_id_post_data_Success_EmptyBody():
        url = BASE_URL + "todos/{id}"    

        response = requests.get(url.format(id = 1))

        assert response.status_code == 200

        data = response.json()['todos'][0]

        title = data['title']
        DS = data['doneStatus']
        desc = data['description']

        data = { }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 200

        data = response.json()

        assert data['title'] == title
        assert data['doneStatus'] == DS
        assert data['description'] == desc
        
# Post to todo page contents will only title
def test_todo_id_post_data_Success_TitleOnly():
        url = BASE_URL + "todos/{id}"  
        
        response = requests.get(url.format(id = 1))

        data1 = response.json()['todos'][0]

        title = data1['title']
        DS = data1['doneStatus']
        desc = data1['description']

        data = {"title":"JCBTestTitle" }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 200

        data = response.json()

        assert data['title'] == "JCBTestTitle"
        assert data['doneStatus'] == DS
        assert data['description'] == desc

# Post to todo page contents will only title
def test_todo_id_post_data_Success_DescriptionEmpty():
        url = BASE_URL + "todos/{id}"  
        
        response = requests.get(url.format(id = 1))

        data = response.json()['todos'][0]

        title = data['title']
        DS = data['doneStatus']
        desc = data['description']

        data = {"title":"JCBTestTitle" , "description": ""}

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 200

        data = response.json()

        assert data['title'] == "JCBTestTitle"
        assert data['doneStatus'] == DS
        assert data['description'] == ""

# Post to todo id without specifying id
def test_todo_id_post_data_Fail_ID():
        url = BASE_URL + "todos/{id}"    

        data = { }

        response = requests.post(url, json = data)

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["No such todo entity instance with GUID or ID {id} found"]}

# Post to todo page contents with empty title
def test_todo_id_post_data_Fail_BadID():
        url = BASE_URL + "todos/{id}"   

        data = {
                "title": "blah",
                "doneStatus": False,
                "description": "descriptiontest"
                }

        response = requests.post(url.format(id = 159), json = data)

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["No such todo entity instance with GUID or ID 159 found"]}

# Post to todo page contents with empty title
def test_todo_id_post_data_Fail_TitleEmpty():
        url = BASE_URL + "todos/{id}"   

        data = {
                "title": "",
                "doneStatus": False,
                "description": "descriptiontest"
                }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["Failed Validation: title : can not be empty"]} 

# Post to todo page contents with malformed boolean input| Malformed JSON body
def test_todo_id_post_data_Fail_Bool():
        url = BASE_URL + "todos/{id}"    

        data = {
                "id": 1,
                "title": "blahblah",
                "doneStatus": "False",
                "description": "descriptiontest"
                }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["Failed Validation: doneStatus should be BOOLEAN"]} 


# Post to todo page contents with a bad key| Testing for malformed json body
def test_todo_id_post_data_Fail_BadKey():
        url = BASE_URL + "todos/{id}"   

        data = {"bobbyMcgee":"Janis Joplin" }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["Could not find field: bobbyMcgee"]} 


# patch todo test | Undocumented
def test_todo_id_patch():
        url = BASE_URL + "todos/{id}"   

        response = requests.patch(url)

        assert response.status_code == 405

# Put todo/id test with full body
def test_todo_id_put_Success_full():
        url = BASE_URL + "todos/{id}"  

        data = {
                "id" : 1,
                "title": "titletestjcb",
                "doneStatus": False,
                "description": "descriptiontestjcb"
                }

        response = requests.put(url.format(id = 1), json = data)

        assert response.status_code == 200

        data = response.json()
        assert data['title'] == 'titletestjcb'
        assert data['doneStatus'] == 'false'
        assert data['description'] == "descriptiontestjcb"

# Put todo/id test with only title
def test_todo_id_put_Success_title():
        url = BASE_URL + "todos/{id}"  

        data = {
                "title": "titletestjcb123",
                }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 200

        data = response.json()
        assert data['title'] == 'titletestjcb123'


# Put todo/id test with no ID
def test_todo_id_put_Fail_ID():
        url = BASE_URL + "todos/{id}"  

        response = requests.put(url)

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["Invalid GUID for {id} entity todo"]} 

# Put todo/id test with no Body
def test_todo_id_put_Fail_Body():
        url = BASE_URL + "todos/{id}"  

        data = {}

        response = requests.put(url.format(id = 1), json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["title : field is mandatory"]}  


# Succesffuly create, then delete, then check for an id
def test_todo_id_delete():
        url = BASE_URL + "todos/{id}"    

        data ={"title":"deleteTest"}

        response = requests.post(BASE_URL+"todos",json = data)

        data = response.json()

        ID = data['id']

        assert data['title'] == "deleteTest"

        response = requests.delete(url.format(id = ID))

        assert response.status_code == 200

        response = requests.get(url.format(id = ID))

        assert response.status_code == 404

# Fail to delete due to no Id given
def test_todo_id_delete_fail_noID():
        url = BASE_URL + "todos/{id}"    

        response = requests.delete(url)

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["Could not find any instances with todos/{id}"]} 

# Fail to delete due to invalid ID given
def test_todo_id_delete_fail_BadID():
        url = BASE_URL + "todos/{id}"    

        response = requests.delete(url.format(id = 9999))

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["Could not find any instances with todos/9999"]} 

# options todo/:id test | Undocumented
def test_todo_id_options():
        url = BASE_URL + "todos/{id}"    

        response = requests.options(url)

        assert response.status_code == 200


### TODOS/:ID/CATEGORIES SECTION

# Get the todo category page contents by id
def test_todo_id_categories_get_data():
    url = BASE_URL + "todos/{id}/categories"  
    
    response = requests.get(url.format(id = 2))

    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()

    assert 'categories' in data


# Get the todo category page contents without specifying an id
def test_todo_id_categories_get_data_noId():
    url = BASE_URL + "todos/{id}/categories"  
    
    response = requests.get(url)

    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()

    assert 'categories' in data


# Get the todo category page contents of a todo that has no categories
def test_todo_id_categories_get_data_noCategory():

    url = BASE_URL + "todos/{id}"

    data = {"title":"deleteTest"}

    response = requests.post(BASE_URL+"todos",json = data)

    data = response.json()

    ID = data['id']

    url = BASE_URL + "todos/{id}/categories"  

    response = requests.get(url.format(id = ID))

    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()['categories']

    assert data == []

# Get Head information for todo category with ID
def test_todo_id_categories_head_data_body():
    url = BASE_URL + "todos/{id}/categories"  

    response = requests.head(url.format(id = 1))
    
    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response content type is text/html
    assert response.headers['Content-Type'] == 'application/json'


# Post to todo categories page contents will all inputs
def test_todo_id_categories_post_data_Success_FullBody():
        url = BASE_URL + "todos/{id}/categories"  

        data = {
                "title": "titletestjcb",
                "description": "descriptiontestjcb"
                }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 201

        data = response.json()
        assert data['title'] == 'titletestjcb'
        assert data['description'] == "descriptiontestjcb"

        
# Post to todo page contents will only title
def test_todo_id_categories_post_data_Success_TitleOnly():
        url = BASE_URL + "todos/{id}/categories"    

        data = {"title":"JCBTestTitle" }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 201

        data = response.json()

        assert data['title'] == "JCBTestTitle"


# Post to todo id without specifying id
def test_todo_id_categories_post_data_Fail_ID():
        url = BASE_URL + "todos/{id}/categories"      

        data = { }

        response = requests.post(url, json = data)

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["Could not find parent thing for relationship todos/{id}/categories"]} 


# Post to todo page contents with empty body
def test_todo_id_categories_post_data_Fail_TitleEmpty():
        url = BASE_URL + "todos/{id}/categories"      

        data = { }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 400

        assert response.json() == {"errorMessages":["title : field is mandatory"]} 


# Post to todo page contents with a bad key| Testing for malformed json body
def test_todo_id_categories_post_data_Fail_BadKey():
        url = BASE_URL + "todos/{id}/categories"    

        data = {"id": 1 }

        response = requests.post(url.format(id = 1), json = data)

        assert response.status_code == 404

        assert response.json() == {"errorMessages":["Could not find thing matching value for id"]} 


# patch todo test | Undocumented
def test_todo_id_categories_patch():
        url = BASE_URL + "todos/{id}/categories"    

        response = requests.patch(url)

        assert response.status_code == 405


# Put todo/id test with no ID | Undocumented
def test_todo_id_categories_put_Fail_ID():
        url = BASE_URL + "todos/{id}/categories"   

        response = requests.put(url)

        assert response.status_code == 405


# Delete todo category | Undocumented
def test_todo_id_categories_delete():
        url = BASE_URL + "todos/{id}/categories"   

        response = requests.delete(url)

        assert response.status_code == 405


# options todo/:id test | Undocumented
def test_todo_id_categories_options():
        url = BASE_URL + "todos/{id}/categories"      

        response = requests.options(url)

        assert response.status_code == 200


""" 
def test_shutdown():
        url = BASE_URL + "shutdown"

        response = requests.get(url)

"""
